from typing import Dict, overload
import pygame
from pygame.sprite import Group, spritecollide, collide_mask

class Card(Group):
    """
    A class to represent a single card of a collection of symbols.

    Attributes:
        TODO

    Methods:
        TODO
    """

    def __init__(self, symbols, radius, symbols_per_card) -> None:
        """
        Constructor for Card class.

        Parameters:
            symbols (List): List of instances of Symbol.
            radius (int): Radius of a single card in pixels.
            symbols_per_card (int): Number of symbols per card
        """
        # Raise exception if number of sprites and symbol_per_card not equal
        if len(symbols) != symbols_per_card:
            raise Exception("Number of sprites supplied does not equal the symbols_per_card.")
        
        super().__init__(*symbols)
        self.collisions = {} # A dictionary that will hold information on collisions between symbols
        self.radius = radius # Radius of the card
        self.symbols_per_card = symbols_per_card

    def copy(self):
        """copy a group with all the same sprites

        Group.copy(): return Group

        Returns a copy of the group that is an instance of the same class
        and has the same sprites in it.

        """
        return self.__class__(  # noqa pylint: disable=too-many-function-args
            self.sprites(), radius=self.radius, symbols_per_card=self.symbols_per_card  # Needed because copy() won't work on AbstractGroup
        )

    def regenerate(self):
        """
        Regenerates all symbols in the card by randomise the positions and sizes of them.
        """
        
        for s in self:
            # Randomise position
            pass

    

    def calc_collisions(self) -> Dict:
        """
        Returns a dictionary of each symbol and a list of symbols in the same card that it collides with.

        Returns:  
            collisions (Dict): A dictionary of collisions. Key = a symbol in the card, Value = List of all symbols in same card that collides with it
        """
        card_copy = self.copy() # Create a copy of the card
        self.collisions = {}
        for sprite in self:
            card_copy.remove(sprite) # Remove sprite from the copy, so not checking on collisions with itself (which will always be True)
            self.collisions[sprite] = spritecollide(sprite, card_copy, False, collide_mask) # Check for collision of sprite with any other sprite
            card_copy = self.copy() # Refresh the copy before the next loop

        return self.collisions
        