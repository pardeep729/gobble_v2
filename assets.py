import math
import os

import pygame
from pygame.transform import scale


####################
# Helper functions #
####################

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


###########
# Classes #
###########

class Assets():
    """
    A class to represent assets of the pygame app.

    Attributes:
        directory (str): Directory of source images
        images (list(dict)): Stores all image surfaces, along with other attributes
    
    Methods:
        normalise_images -> None: Normalises the size of all image surfaces depending on the card size and number of symbols per card
        get_asset_from_name
    """

    def __init__(self, directory_rel: str) -> None:
        """
        Constructor for Assets class.

        Parameters:
            directory_rel (str): Relative path to folder containing images. Default = "Images"
        """
        self.directory = abs_path(directory_rel) # Absolute path to folder

        # Gather file titles, paths and generate surfaces
        filenames = os.listdir(self.directory)
        self.images = []
        for fn in filenames:
            file_path = os.path.join(self.directory, fn)
            file = {
                'Name': fn.split('.')[0], 
                'File path': file_path,
                'Surface': pygame.image.load(file_path),
                'Is Normalised?': False
            }
            self.images.append(file)

    def normalise_images(self, card_radius: int, symbols_per_card: int) -> None:
        """
        Normalises the area of each image Surface, so they all originally have an equal share of the window. Maintains ratio.

        Notes:
        ------
        old_area, old_width, old_height = Area, width and height of the surface origially
        new_area = 2 * card_radius * (1/symbols_per_card)
        scale_factor = new_area / old_area
        new_width = old_width * scale_factor
        new_height = old_height * scale_factor

        Parameters:
            radius (int): Radius of a single card in pixels.
            symbols_per_card (int): Number of symbols per card
        """

        new_area = (2 * card_radius)**2 * (1/symbols_per_card) # Target new area for each image
        
        for idx, i in enumerate(self.images):
            # "Old" image attributes
            old_surf = i['Surface']
            old_width = old_surf.get_width()
            old_height = old_surf.get_height()
            old_area = old_width * old_height

            scale_factor = math.sqrt(new_area / old_area) # Scale factor for current image

            # New attributes
            new_width = math.floor(old_width * scale_factor)
            new_height = math.floor(old_height * scale_factor)

            new_surf = scale_img(old_surf, (int(new_width), int(new_height)))
            
            # Replace surface and set "is normalised" to True for current image
            self.images[idx]['Surface'] = new_surf
            self.images[idx]['Is Normalised?'] = True


    def get_asset_from_name(self, name: str) -> dict:
        """
        Return the specific asset dict based on name of it

        Parameters:
            name (str): Value of the asset dict 'name' attribute

        Returns:
            asset (dict): Target asset dict 
            Raise Exception if does not exist 
        """

        asset = None
        for a in self.images:
            if a['Name'] == name:
                asset = a
                return asset
        
        raise Exception(f"{name} does not exist in this Assets instance.")

    def get_assets_from_name(self, names: list[str]) -> list[dict]:
        """
        Return a list of the specific asset dicts based on names supplied

        Parameters:
            names (List(str)): Values of the asset dict 'name' attribute

        Returns:
            assets (List(dict)): Target asset dicts 
        """

        assets = []
        for n in names:
            assets.append(self.get_asset_from_name(n))
        return assets