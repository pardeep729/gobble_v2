import pygame
from pygame.sprite import Sprite


class Symbol(Sprite):
    """
    A class to represent a single symbol on a gobble card.

    Attributes:
        TODO

    Methods:
        TODO
    """
    
    def __init__(self, name, image_path_abs: str, width=None, height=None, 
                    pos_x=0, pos_y=0, angle=0, scale=1) -> None:
        """
        A class to represent a single symbol of a gobble card.

        Parameters:
            name (str): Identifiable name of the symbol
            image_path_abs (str): Absolute path to the image of the symbol
            TODO
        """
        super().__init__()
        self.name = name # Name of the symbol
        self.image_path_abs = image_path_abs # Absolute path to image of the symbol
        self.width = width # Desired new width in pixels. Leave as None to keep image unscaled
        self.height = height # Desired new height in pixels. Leave as None to keep image unscaled
        self.angle = angle # Angle to rotate image by relative to how image was loaded, in degrees
        self.scale = scale # Scale the image, on top of the "original" width/height specified

        self.image = pygame.image.load(self.image_path_abs) # Load image as a Surface object

        # Rescale image
        if width is not None and height is not None:
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # Apply scale factor
        self.image = pygame.transform.scale(self.image, 
            (self.scale*self.image.get_width(), self.scale*self.image.get_height())
        )

        self.image = pygame.transform.rotate(self.image, self.angle) # Rotate image

        self.rect = self.image.get_rect() # Rect attribute of the symbol
        self.rect.x = pos_x # X coordinate of position of symbol on screen
        self.rect.y = pos_y # Y coordinate of position of symbol on screen

        self.mask = pygame.mask.from_surface(self.image) # Create a mask of the Surface object of this symbol
        
    def get_pos(self) -> tuple:
        """
        Return tuple of the x and y position of the symbol.

        Returns:
            (pos_x, pos_y) (tuple): X and Y position of the symbol
        """
        pos_x = self.pos_x
        pos_y = self.pos_y
        return (pos_x, pos_y)

    def get_surf():
        """
        Return the Surface object of the symbol

        Returns:
            surf (Surface): Surface object of the symbol
        """
        return self.image

    def get_mask():
        """
        Return the mask object of the symbol

        Returns:
            mask (Mask): Mask object of the surface of the symbol
        """
        return self.mask






