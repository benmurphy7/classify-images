import tensorflow as tf
import sys
import os

if not os.path.exists("Images"):
    os.makedirs("Images/")
    print("Images folder created.")
else:
    print("Extracting images from folders...")
    # Extract images from folders
    f_count = 0
    d_count = 0
    for root, dirs, files in os.walk("Images"):
       for file in files:
            f_count +=1
            f_path = os.path.join(root,file)

            # Strip copy label (x) from file name ex: IMG_0001 (x).JPG
            name = os.path.splitext(file)[0].split(" ")[0]
            extension = os.path.splitext(file)[1]
            n_path = "Images/" + name + extension

            # Check for duplicate filename in root
            if os.path.realpath(n_path) == os.path.realpath(f_path):
                pass
            elif not os.path.exists(n_path):
                os.rename(f_path, os.path.realpath(n_path))
            else:
                for copy in range (1,100,1):
                    t_path = "Images/" + name + " ({})".format(copy) + extension
                    if not os.path.exists(t_path):
                        os.rename(f_path, t_path)
                        break
    if f_count == 0:
        print ("Images folder empty.")
    else:
        print("Done")

    print("\nRemoving empty folders...")

    # Remove empty folders
    def removeEmptyFolders(path, removeRoot=True):
      global d_count
      if not os.path.isdir(path):
        return

      # Get subfolder paths
      files = os.listdir(path)
      if len(files):
        for f in files:
          fullpath = os.path.join(path, f)
          if os.path.isdir(fullpath):
            removeEmptyFolders(fullpath)

      # Delete empty folders
      files = os.listdir(path)
      if len(files) == 0 and removeRoot and not path=="Images":
        print ("Removing empty folder: " + path)
        os.rmdir(path)
        d_count +=1

    removeEmptyFolders("Images")
    if d_count == 0:
        print ("No empty folders found.\n")
    else:
        print("Done\n")

    # Select all files
    onlyfiles = [f for f in os.listdir("Images") if os.path.isfile(os.path.join("Images", f))]


    # Load label file, strip off carriage return
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("retrained_labels.txt")]

    # Make label folders
    for l in label_lines:
        if not os.path.exists("Sorted/" + str(l)):
            os.makedirs("Sorted/" + str(l))

    # Unpersist graph from file
    with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    # Classify and sort images
    with tf.Session() as sess:
        p_count = 1
        for f in onlyfiles:
            file_name = str(f)
            name = os.path.splitext(f)[0]
            image_path = "Images/" + file_name
            image_data = tf.gfile.FastGFile(image_path, 'rb').read()

            print ("\n[{}/{}] Classifying ".format(str(p_count),str(f_count)) + file_name)


            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

            predictions = sess.run(softmax_tensor, \
                                   {'DecodeJpeg/contents:0': image_data})

            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

            node_id = top_k[0]
            human_string = label_lines[node_id]
            score = predictions[0][node_id]

            print (str(score*100) + " " + human_string)
            print ("Location:  ", end="")
            rename = str(round(score*100,3)) + " (" + human_string + ") "
            win_name = rename + name
            rename = rename + file_name
            new_path = "Sorted/{}/{}".format(human_string,rename)
            win_path = "Sorted/{}/{}".format(human_string,win_name)
            print (new_path)
            if not os.path.exists(new_path) and not os.path.exists(win_path):
                os.rename(image_path, new_path)
                if p_count == f_count:
                    print ("\nDone")
            else:
                os.remove(image_path)
                print ("Duplicate detected: Image removed")

            p_count += 1




