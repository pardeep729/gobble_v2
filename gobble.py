# Standard modules
import time

# Installed modules
import pygame
from pygame.sprite import groupcollide, spritecollide, collide_rect, collide_mask


# Custom modules
from assets import make_path, Assets
from autocropper import AutoCropper
from symbol import Symbol
from card import Card


# Initialise pygame
pygame.init()


# Global variables
APP_NAME = 'Gobble Generator 2' # Name of app
WINDOW_WIDTH = 1000 # Width of window
WINDOW_HEIGHT = WINDOW_WIDTH # Height of window (square)
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW = None # Global instance of window Surface
FPS = 60 # Frames per second
CARD_RADIUS = WINDOW_WIDTH / 2 # Radius of each card (=1/2 width of window)
SYMBOLS_PER_CARD = 8 # Number of symbols per card 

def main():
    """
    This function is executed when main.py is run

    Flow: TODO Finish
        1. Load all assets (images) into memory and normalise sizes
        2. Create the base pygame app
        3.  ....
    """

    #################
    # Preliminaries #
    #################

    # Make sure all images are cropped to their content (i.e. no empty space around each image)
    autocropper = AutoCropper('images')
    autocropper.crop('images_cropped')

    # Load all images
    assets = Assets('images_cropped')
    assets.normalise_images(CARD_RADIUS, SYMBOLS_PER_CARD)

    # Set title and window size
    pygame.display.set_caption(APP_NAME)
    WINDOW = pygame.display.set_mode(WINDOW_SIZE)

    # Set clock
    clock = pygame.time.Clock()
    
    # Start run loop
    run = True

    #################
    # Main run loop #
    #################

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
        # Update necessary things # 
        # (e.g. variables)        #
        ###########################

        #################
        # Draw graphics #
        #################

        # Draw an example card

        assets_for_card = assets.get_assets_from_name(
            ['MANGO', 'CRANE', 'DARTH VADER', 'GORILLA', 'REKHAS CHILLI', 'MR BURNS', 'GINGY', 'GLASSI']
        ) # Get chosen images
        sprites = []
        for idx, a in enumerate(assets_for_card):
            sprites.append(Symbol(
                a, 
                pos_x=idx*(WINDOW_WIDTH/SYMBOLS_PER_CARD),
                pos_y=idx*(WINDOW_HEIGHT/SYMBOLS_PER_CARD),
                scale=0.3
            )) 
        card1 = Card(sprites, radius=CARD_RADIUS, symbols_per_card=SYMBOLS_PER_CARD)
        
        # Draw card circle
        pygame.draw.circle(WINDOW, 
            (255, 255, 255), 
            (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            card1.radius
        )
        card1.draw(WINDOW) # Draw card symbols

        
        collisions = card1.calc_collisions() # Calculate collisions

        # Print out collisions
        for sprite_a, colliding_sprites in collisions.items():
            if len(colliding_sprites) > 0:
                for sprite_b in colliding_sprites:
                    print(f"{sprite_a.name} colliding with {sprite_b.name}")
            # else:
            #     print(f"{sprite_a.name} doesn't collide with anything")
        
        
        # break
        
        ##########################
        # Last things to execute #
        ##########################
        pygame.display.update()
        pygame.display.flip()





# App starts here
if __name__ == '__main__':
    main()

"""
Help:
https://pythonprojects.io/space-shooter-tutorial
https://pythonprogramming.altervista.org/using-pygame-sprite-collide_masksprite1-sprite2-for-collision-detection-in-pygame/
https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.groupcollide
https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.collide_mask
"""