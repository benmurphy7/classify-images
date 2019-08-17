# Run next to Annotations and Images folders

import os


if not os.path.exists("Annotations"):
    print("Missing Annotations Folder")
if not os.path.exists("Images"):
    print("Missing Images Folder")

# Extract images from folders
for x in range (0,2):
    folder = ""
    if x==0:
        folder = "Images"
    else:
        folder = "Annotations"
    print("Extracting files from " + folder + " folder...")
    f_count = 0
    d_count = 0
    for root, dirs, files in os.walk(folder):
       for file in files:
            f_count +=1
            f_path = os.path.join(root,file)

            # Strip copy label (x) from file name ex: IMG_0001 (x).JPG
            name = os.path.splitext(file)[0].split(" ")[0]
            extension = os.path.splitext(file)[1]
            n_path = folder + "/" + name + extension

            # Check for duplicate filename in root
            if os.path.realpath(n_path) == os.path.realpath(f_path):
                pass
            elif not os.path.exists(n_path):
                os.rename(f_path, os.path.realpath(n_path))
            else:
                for copy in range (1,100,1):
                    t_path = folder + "/" + name + " ({})".format(copy) + extension
                    if not os.path.exists(t_path):
                        os.rename(f_path, t_path)
                        break
    if f_count == 0:
        print (folder + " folder empty.")


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
      if len(files) == 0 and removeRoot and not path==folder:
        print ("Removing empty folder: " + path)
        os.rmdir(path)
        d_count +=1

    removeEmptyFolders(folder)
    if d_count == 0:
        print ("No empty folders found.\n")
    else:
        print("Done\n")
