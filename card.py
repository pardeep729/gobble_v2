import math
import multiprocessing
import numpy as np
import random
from typing import Dict, overload
from deprecated import deprecated

import pygame
from pygame.sprite import Group, spritecollide, collide_mask

from symbol import Symbol

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
            symbols (list(Symbol)): List of instances of Symbol.
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

        # Arrangements dictionary
        self.arrangements_templates = [
            # {'Outside': self.symbols_per_card, 'Inside': 0},
            {'Outside': self.symbols_per_card - 1, 'Inside': 1},
            {'Outside': self.symbols_per_card - 2, 'Inside': 2}
        ]

    def copy(self):
        """copy a group with all the same sprites

        Group.copy(): return Group

        Returns a copy of the group that is an instance of the same class
        and has the same sprites in it.

        """
        return self.__class__(  # noqa pylint: disable=too-many-function-args
            self.sprites(), radius=self.radius, symbols_per_card=self.symbols_per_card  # Needed because copy() won't work on AbstractGroup
        )

    def replace_symbol(self, old_symbol: Symbol, new_symbol: Symbol) -> None:
        """
        Replace the specified old Symbol instance with the new one
        
        Parameters:
            old_symbol (Symbol): The Symbol instance to be replaced
            new_symbol (Symbol): The Symbol instance to add
        """

        # Raise exceptions if the parameters are not valid
        if not self.has(old_symbol):
            raise Exception(f"{old_symbol} is not a member of this card")
        
        if not isinstance(old_symbol, Symbol): 
            raise Exception(f"{old_symbol} is not an instance of Symbol")
        
        if not isinstance(new_symbol, Symbol):
            raise Exception(f"{new_symbol} is not an instance of Symbol")

        # Replace if the above didn't raise any exceptions
        self.remove(old_symbol)
        self.add(new_symbol)
    

################################################
# TODO: Find the best "regeneration" algorithm #
################################################
    @deprecated("Use v2")
    def regenerate_card_v1(self):    
        """
        Rgeenerate all symbols in the card with new random positions, scales and rotations
        """

        # Randomise how many big, medium and small ones there should be. At least 1 of each required
        big, medium, small = 0, 0, 0
        while (big < 1 or medium < 1 or small < 1):
            big = random.randint(0, self.symbols_per_card) # Randomise number of big ones
            small = random.randint(0, self.symbols_per_card-big) # Randomise number of small ones from remainder
            medium = self.symbols_per_card - big - small # Mediums are the remainder

        # Create a "big, medium or small" list. Shuffle it
        sizes = []
        sizes.extend(['big' for _ in range(big)])
        sizes.extend(['medium' for _ in range(big)])
        sizes.extend(['small' for _ in range(big)])
        random.shuffle(sizes)

        # Scale bounds based on the "size" label
        size_scale_bounds = {
            'big': (0.6, 0.7),
            'medium': (0.5, 0.6),
            'small': (0.4, 0.5)
        }

        for idx, (old_symbol, size) in enumerate(zip(self, sizes)):
            # Randomise position
            r = random.randint(0, self.radius*0.9) # Distance from centre of circle, limited by card radius
            theta = (idx+1) * random.randint(0, 360/self.symbols_per_card) # Polar angle, in radians
            pos_x = self.radius + r*math.cos(math.radians(theta)) # x = r × cos( θ )
            pos_y = self.radius + r*math.sin(math.radians(theta)) # y = r × sin( θ )

            # Random scale
            scale_bounds = size_scale_bounds.get(size) # Get bounds for the current "size"
            offset = scale_bounds[0] # Offset of scale range will be the lower bound
            spread = scale_bounds[1] - scale_bounds[0] # Range will be the spread between both bounds
            scale = random.random()*spread + offset

            # Random angle in degrees
            angle = random.randint(0, 360)

            new_symbol = Symbol(
                old_symbol.asset, pos_x, pos_y, angle, scale,
            )

            self.replace_symbol(old_symbol, new_symbol)

    def regenerate_card_v2(self):
        """
        Regenerate cards. 
        
        - Choose 1 of a few "home position" arrangements. 
        - Add noise to radial positions and polar angles
        - Randomise scale and rotation for each symbol

        """

        # Randomise how many big, medium and small ones there should be. At least 1 of each required
        big, medium, small = 0, 0, 0
        while (big < 1 or medium < 1 or small < 1):
            big = random.randint(0, self.symbols_per_card) # Randomise number of big ones
            small = random.randint(0, self.symbols_per_card-big) # Randomise number of small ones from remainder
            medium = self.symbols_per_card - big - small # Mediums are the remainder

        # Create a "big, medium or small" list. Shuffle it
        sizes = []
        sizes.extend(['big' for _ in range(big)])
        sizes.extend(['medium' for _ in range(big)])
        sizes.extend(['small' for _ in range(big)])
        random.shuffle(sizes)

        # Scale bounds based on the "size" label
        size_scale_bounds = {
            'big': (0.65, 0.7),
            'medium': (0.55, 0.65),
            'small': (0.40, 0.55)
        }

        # Choose random arrangement
        arrangement_template = random.choice(self.arrangements_templates)
        no_outside = arrangement_template.get('Outside') # No of symbols on outer rim
        no_inside = arrangement_template.get('Inside') # No of symbols in inner rim

        arrangements = []
        arrangements.extend(['outside' for _ in range(no_outside)])
        arrangements.extend(['inside' for _ in range(no_inside)])
        random.shuffle(arrangements)

        r_boundary = 0.5 # Boundary between "inner" and "outer" rim, as fraction of total radius of card

        # Keeps track of how many of each rim's symbols we've already placed
        inside_counter = 0
        outside_counter = 0
        for idx, (old_symbol, arrangement, size) in enumerate(zip(self, arrangements, sizes)):
            # Set some parameters, depending on rim assigment
            if arrangement == 'inside':
                r_bounds = (0.0, self.radius*r_boundary)
                no_in_rim = no_inside
                inside_counter += 1
                temp_counter = inside_counter
            elif arrangement == 'outside':
                r_bounds = (self.radius*r_boundary, 0.9*self.radius)
                no_in_rim = no_outside
                outside_counter += 1
                temp_counter = outside_counter
            
            # Randomise radius within boundaries
            r = random.randint(*r_bounds) # Distance from centre of circle, limited by r_bounds

            # Set home theta, add random noise within a range
            theta = 360 if no_in_rim == 0 else 360 * (temp_counter/no_in_rim) 
            noise_boundary = int((1/4) * (360 if no_in_rim == 0 else 360 / no_in_rim))
            noise = random.randint(-noise_boundary, noise_boundary)
            theta += noise

            # Set position
            pos_x = self.radius + r*math.cos(math.radians(theta)) # x = r × cos( θ )
            pos_y = self.radius + r*math.sin(math.radians(theta)) # y = r × sin( θ )

            # Random scale
            scale_bounds = size_scale_bounds.get(size) # Get bounds for the current "size"
            offset = scale_bounds[0] # Offset of scale range will be the lower bound
            spread = scale_bounds[1] - scale_bounds[0] # Range will be the spread between both bounds
            scale = random.random()*spread + offset

            # Random angle in degrees
            angle = random.randint(0, 360)

            new_symbol = Symbol(
                old_symbol.asset, pos_x, pos_y, angle, scale,
            )

            self.replace_symbol(old_symbol, new_symbol)


    def card_ratio_cover(self):
        """
        Calculates the sum of the areas of all symbols and calculations the fraction of the total card area
        """

        ratio = 0 # Start with symbols covering none of the card by default

        area_card = math.pi * self.radius**2 # Area of card

        # Area of symbols
        area_symbols = 0 # Keep track of running total of areas
        for s in self:
            pixel_array = pygame.surfarray.array_alpha(s.image).flatten() # Turn surface into 1d array
            filled_array = [0 if pixel == 0 else 1 for pixel in pixel_array] # Make sure only 1s and 0s in array
            area = sum(filled_array) # Sum
            area_symbols += area # Add to running total
 
        ratio = area_symbols/area_card # Calculate ratio
        # print(ratio)

        return ratio
 ########################
 # ########################
 # ########################   



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

    def has_collisions(self) -> bool:
        """
        Returns True if atleast 2 symbols are colliding. Useful for while loops and if statements.
        Use self.collisions (dict) to work out what exactly is colliding

        Returns:
            has_collisions (bool): True if there is atleast 1 collisions.
        """
        has_collisions = False # Default there are no collisions

        for k, v in self.collisions.items():
            if len(v) != 0:
                has_collisions = True # If at least 1 collision, then return True
                break
        
        return has_collisions
        