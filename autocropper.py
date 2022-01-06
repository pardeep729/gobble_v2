import os
from PIL import Image

from assets import abs_path

class AutoCropper:
    """
    Autocrop all images in supplied directory to content (i.e. no blank space around any image)

    Attributes:
        source_directory (str): Directory of source files
        target_directory (str): Directory of cropped files
        filenames (List(str)): Filenames of source files
        source_filepaths(List(str)): Filepaths of source files
    
    Methods:
        crop -> None: Crops all source files and outputs to target directory.

    """

    def __init__(self, source_directory_rel: str) -> None:
        """
        Constructor for AutoCropper class.
        
        Parameters:
            directory_rel (str): Relative path to source directory
        """
        self.source_directory = abs_path(source_directory_rel) # Absolute path to folder
        self.target_directory = None # It will hold arget path for cropped folders
        self.filenames = os.listdir(self.source_directory) # List of filenames
        self.source_filepaths = [os.path.join(self.source_directory, fn) for fn in self.filenames] # List of filepaths

    def crop(self, target_diretory_rel: str) -> None:
        """
        Crop all images and outputs to chosen target directory

        Parameters:
            target_directory_rel (str): Relative target directory folder name.
        """
        self.target_directory = abs_path(target_diretory_rel)

        # Create directory if does not exist
        if not os.path.exists(self.target_directory):
            os.makedirs(self.target_directory)

        # Iterate over all files
        for fn, fp in zip(self.filenames, self.source_filepaths):
            target_path = os.path.join(self.target_directory, fn)
            if not os.path.exists(target_path):
                image = Image.open(fp) # Load source image
                imageBox = image.getbbox() # Get box around content
                cropped = image.crop(imageBox) # Crop to content
                cropped.save(target_path) # Output cropped image to target directory