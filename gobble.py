# Standard modules
import os
import random
import time

# Installed modules
import pandas as pd
import pygame
from pygame.colordict import THECOLORS as Colours
from pygame.sprite import Sprite, groupcollide, spritecollide, collide_rect, collide_mask


# Custom modules
from assets import make_path, abs_path, Assets
from autocropper import AutoCropper
from symbol import Symbol
from card import Card


# Initialise pygame
pygame.init()


# Global variables
APP_NAME = 'Gobble Generator 2' # Name of app
CARD_RADIUS = 500 # Radius of each card
RING_RADIUS = CARD_RADIUS*1.05
WINDOW_WIDTH = 2*RING_RADIUS # Width of window
WINDOW_HEIGHT = WINDOW_WIDTH # Height of window (square)
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW = pygame.display.set_mode(WINDOW_SIZE) # Global instance of window Surface
FPS = 60 # Frames per second
# CARD_RADIUS = WINDOW_WIDTH / 2 # Radius of each card (=1/2 width of window)
SYMBOLS_PER_CARD = 8 # Number of symbols per card
INPUT_FOLDER_NAME = 'images'
INPUT_FOLDER = abs_path(INPUT_FOLDER_NAME)
OUTPUT_FOLDER_NAME = 'export'
OUTPUT_FOLDER = abs_path(OUTPUT_FOLDER_NAME)
GOBBLE_TEMPLATE_FOLDER = 'template'
GOBBLE_TEMPLATE_FILENAME = 'gobble.xlsx'
GOBBLE_TEMPLATE = make_path(GOBBLE_TEMPLATE_FOLDER, GOBBLE_TEMPLATE_FILENAME)


def main():
    # Check that an export folder exists
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER) 

    ###########################################################
    # Load in dobble template, do necessary name replacements #
    ###########################################################
    raw = pd.read_excel(GOBBLE_TEMPLATE, sheet_name=['Template', 'Replacements'])
    template = raw['Template'] # Dobble template with dobble symbol names
    replacements = raw['Replacements'] # Replacements mapping TODO: take file names and map randomly, if user does not want to set it
    
    replacement_dict = {} # Declare replacement dict
    # Populate dict
    for temp_item, repl_item in zip(replacements.to_dict()['List of Items'].values(), replacements.to_dict()['To Replace With'].values()):
        replacement_dict[temp_item] = repl_item

    customised_template = template.replace(replacement_dict) # Replace template with our values

    #################
    # Preliminaries #
    #################

    # Make sure all images are cropped to their content (i.e. no empty space around each image)
    autocropper = AutoCropper(INPUT_FOLDER_NAME)
    autocropper.crop(f'{INPUT_FOLDER_NAME}_cropped')

    # Load all images
    assets = Assets(f'{INPUT_FOLDER_NAME}_cropped')
    assets.normalise_images(CARD_RADIUS, SYMBOLS_PER_CARD)

    # Load static images too, create sprites for each (use Symbol class so mask generated automatically)
    static_images = Assets('static_images')
    static_images.normalise_images(CARD_RADIUS, 1) # Make sure each of these static images are the same size as the window
    # card_circle = Symbol(static_images.get_asset_from_name('card_circle'), pos_x=WINDOW_WIDTH/2, pos_y=WINDOW_HEIGHT/2)

    # Set title and window size
    pygame.display.set_caption(APP_NAME)
    # WINDOW = pygame.display.set_mode(WINDOW_SIZE)

    clock = pygame.time.Clock() # Game clock

    ###########################################################
    # Load in dobble template, do necessary name replacements #
    ###########################################################
    for i in customised_template.values:
        card_no = i[0]
        symbol_names = i[1:]
        start_time = time.time()
        rim_colour = None
        while rim_colour is None or rim_colour == "white":
            rim_colour = random.choice(list(Colours)) # Randomise colour
        gobble_loop(clock, assets, static_images, card_no, symbol_names, rim_colour)
        end_time = time.time()
        print(f"Card {card_no} took {end_time - start_time} seconds to run.")

    
    
def gobble_loop(clock: pygame.time.Clock, assets: Assets, static_images: Assets,
                card_no: int, symbol_names: list, rim_colour: str):
    """
    This function is executed when main.py is run

    Flow: TODO: Finish
        1. Load all assets (images) into memory and normalise sizes
        2. Create the base pygame app
        3.  ....

    Parameters:
        TODO:
    """

    #################
    # Preliminaries #
    #################
    card_outer = Symbol(static_images.get_asset_from_name('card_outer'), pos_x=WINDOW_WIDTH/2, pos_y=WINDOW_HEIGHT/2) # Outer card surface (for collisions)


    #################
    # Main run loop #
    #################

    run = True # Run while this is true
    is_first_run = True # Do some things once per run, such as create Card instance
    is_card_valid = False # A flag for when a valid card is found

    while run:
        clock.tick(FPS) # Tick clock

        #################
        # Handle events #
        #################

        for event in pygame.event.get():
            # Exit game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


        ###########################
        # Update/create necessary things # 
        # (e.g. variables)        #
        ###########################

        # Create an example card once
        if is_first_run:
            # Get chosen images
            assets_for_card = assets.get_assets_from_name(
                # ['MANGO', 'CRANE', 'DARTH VADER', 'GORILLA', 'REKHAS CHILLI', 'MR BURNS', 'GINGY', 'GLASSI']
                list(symbol_names)
                # ['REKHAS CHILLI', 'MR BURNS', 'GINGY', 'GLASSI']
            ) 

            # Generate Symbol instances with default scale, rotation and position 
            sprites = [Symbol(a) for a in assets_for_card] 
            card = Card(sprites, radius=CARD_RADIUS, symbols_per_card=SYMBOLS_PER_CARD)           

        
        outside_card_circle = spritecollide(card_outer, card, False, collide_mask) # Calculate if any sprite is outside of the card circle
        collisions = card.calc_collisions() # Calculate collisions

        # Regenerate if collisions
        if card.has_collisions() or len(outside_card_circle) > 0:
            # card.regenerate_card_v1() # FIXME: version 1 = regenerate whole card. May find problematic, then can try regenerating specific symbols.
            card.regenerate_card_v2()
        else:
            ratio_cover = card.card_ratio_cover() # Calculate card cover of symbols
            # Regenerate if not enough cover
            if ratio_cover < 0.22: 
                card.regenerate_card_v2()
            else:
                is_card_valid = True # A flag for when a card is valid
        

        # TODO: Make the code quicker
        # TODO: Try some smarter methods
        #       Modify parameters of the noise
        #       Only change the symbols that are colliding, rather than the whole card - hreshold to 10 tries (or something) before regenerating whole card again
        #       Tweak cover threshold



                
        

            # Print out collisions
        #     for sprite_a, colliding_sprites in collisions.items():
        #         if len(colliding_sprites) > 0:
        #             for sprite_b in colliding_sprites:
        #                 print(f"{sprite_a.name} colliding with {sprite_b.name}")  
        # else:
        #     print("No collisions")
            # run = False # TODO: Renable once happy code works

        # Check distribution is good (i.e. not too much whitespace) 
        # TODO: Probably use pixel values and set a threshold of some %


        is_first_run = False # Don't run certain blocks again (e.g. creating card)

        #################
        # Draw graphics #
        #################

        # Show a black background if card is not valid
        if not is_card_valid:
            WINDOW.fill(Colours["black"])
        # Show a white background if card is valid and don't draw the outer_card thing
        else:
            WINDOW.fill(Colours["white"])
        # Clear screen
        

        # Draw card circle and card outer
        # pygame.draw.circle(WINDOW, 
        #     (255, 255, 255), 
        #     (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
        #     card.radius
        # )
        # WINDOW.blit(card_circle.image, card_circle.rect)
        # WINDOW.blit(card_outer.image, card_outer.rect) # Outer boundary (for collision detection)
        pygame.draw.circle(WINDOW, Colours[rim_colour], (WINDOW_WIDTH/2, WINDOW_HEIGHT/2), RING_RADIUS) # Card rim
        pygame.draw.circle(WINDOW, Colours["white"], (WINDOW_WIDTH/2, WINDOW_HEIGHT/2), CARD_RADIUS) # Card circle

        card.draw(WINDOW) # Draw card symbols
            
        # break
        
        ##########################
        # Last things to execute #
        ##########################
        pygame.display.update()
        # pygame.display.flip()

        if is_card_valid:
            pygame.image.save(WINDOW, os.path.join(OUTPUT_FOLDER, f"card_{card_no}.png")) # Export to png
            run = False # Stop run


###################
# App starts here #
###################
if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(f"Program took {end - start} seconds to run.")




"""
Help:
https://pythonprojects.io/space-shooter-tutorial
https://pythonprogramming.altervista.org/using-pygame-sprite-collide_masksprite1-sprite2-for-collision-detection-in-pygame/
https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.groupcollide
https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.collide_mask
"""