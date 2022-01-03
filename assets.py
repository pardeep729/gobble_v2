""" TODO currently unfinished and unimplemented, try ot merge it in when the time is right"""


# Import standard libraries
import os

# Import modules
import pygame



# Helper functions
def abs_path(directory_rel):
    """
    Returns an absolute path to the specified directory

    Parameters:
        directory_rel (str): Relative folder path

    Returns:
        directory_abs (str): Absolute path to the directory
    """
    directory_abs = os.path.join(os.path.dirname(__file__), directory_rel)
    return directory_abs

def make_path(directory_rel, filename):
    """
    Returns an absolute path to the specified directory and filename

    Parameters:
        directory_rel (str): Relative folder path of target file
        filename (str): Name of file in directory

    Returns:
        path (str): Absolute path to the file
    """

    path = ""
    path = os.path.join(abs_path(directory_rel), filename)
    return path

def load_img(directory_rel, filename):
    """
    Returns a pygame Surface object holding the image that was loaded from the specified directory and filename

    Parameters:
        directory_rel (str): Relative folder path of target image file
        filename (str): Name of image file in directory

    Returns:
        surf (Surface): pygame Surface object of the loaded image
    """
    surf = pygame.image.load(make_path(directory_rel, filename))
    return surf

def scale_img(surf, size):
    """
    Returns a pygame Surface object that is a scaled version of the input Surface.

    Parameters:
        surf (Surface): Surface object to be scaled
        size (tuple(2)): New size in pixels. Format = (width (int), height (int))

    Returns:
        surf_scaled (Surface): pygame Surface object of the loaded image
    """
    surf_scaled = None
    surf_scaled = pygame.transform.scale(surf, size)
    return surf_scaled


class Assets():
    """
    A class to represent assets of the pygame app.

    Attributes:
        images (Dict): All custom dobble images. Key = name, value = path to image
    """

    def __init__(self) -> None:
        """
        Constructor for Assets class.
        """
        self.directory_rel = "images"
        self.directory_abs = abs_path(self.directory_rel)
        self.filenames = [i.split('.')[0] for i in os.listdir(self.directory_abs)]
        # self.images = {}