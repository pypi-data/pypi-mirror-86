import os
from PIL import Image

class Renamer():
    """
        Renamer instance to convert images to user defined format
    """
    def __init__(self):
        pass
    
    def null_images(self, folder):
        """
        Removes any null images from a folder
        Args:
            folder (string): folder to look in (preferably with all images)

        Returns:
            None
        """
        for filename in os.listdir(folder):
            if os.stat(filename).st_size == 0:
                os.remove(filename)
                print(filename, "removed")

    def conv_ren(self, folder, form='jpeg', name=None):
        """
            Converts image to format 'form' with the name 'name' in the folder 'folder'
            Args:
                folder (string): folder to look in (preferably with all images)
                form (string): Format to convert to (Default:jpeg)
                name (string): Name to specify for the image (Default:None). If None is specified, 
                then name does not change.  
            Returns:
                None
        """
        i = 1
        self.null_images(folder)
        for filename in os.listdir(folder):
            img = Image.open(os.path.join(folder,filename)).convert("RGB")
            try:
                s = str(name)+"."+str(i)+str(form) if name != None else filename+str(form)
                os.remove(os.path.join(folder,filename))
                img.save(os.path.join(folder,s), form)
                print("Converted", filename, "to", s)
            except Exception:
                print("Check if you have the right format going on. JPG is JPEG. File path should be absolute")
                break
            i += 1
        print("Completed")