# Standard modules
import time

# Installed modules
import pygame
from pygame.sprite import groupcollide, spritecollide, collide_rect, collide_mask


# Custom modules
from assets import make_path, Assets
from symbol import Symbol
from card import Card


# Initialise pygame
pygame.init()


# Global variables
APP_NAME = 'Gobble Generator 2'
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW = None
FPS = 60
CARD_RADIUS = WINDOW_WIDTH / 2

def main():
    """
    This function is executed when main.py is run
    """
    # Set local reference to Assets class
    assets = Assets()
    # print(assets.filenames)

    # Set title and window size
    pygame.display.set_caption(APP_NAME)
    WINDOW = pygame.display.set_mode(WINDOW_SIZE)

    # Set clock
    clock = pygame.time.Clock()
    
    # Start run loop
    run = True

    test_x = 280
    test_y = 150

    while run:
        clock.tick(FPS) # Tick clock
        

        # Handle events
        for event in pygame.event.get():
            # Exit game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


        # Update necessary things (e.g. variables)


        # Draw graphics
        # Draw dobble card circle


        # Draw an example sprite

        symbol_names = ('ADAM', 'AINSLEY', 'AMAL', 'AMAR', 'ANOOP', 'ARIYAN', 'AVOCADO', 'BALJIT')
        symbol1 = Symbol("AINSLEY", make_path('images', 'AINSLEY.png'))   
        symbol2 = Symbol("DARTH VADER", make_path('images', 'DARTH VADER.png'), pos_x=test_x, pos_y=test_y) 
        sprites = [Symbol(sn, make_path("images", sn+".png")) for sn in symbol_names]   
        card1 = Card(sprites, radius=CARD_RADIUS)
        
        # Draw card circle
        pygame.draw.circle(WINDOW, 
            (255, 255, 255), 
            (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            card1.radius
        )
        card1.draw(WINDOW) # Draw card symbols
        print("fine")

        
        collisions = card1.calc_collisions() # Calculate collisions

        # Print out collisions
        for sprite_a, colliding_sprites in collisions.items():
            if len(colliding_sprites) > 0:
                for sprite_b in colliding_sprites:
                    print(f"{sprite_a.name} colliding with {sprite_b.name}")
            else:
                print(f"{sprite_a.name} doesn't collide with anything")
        
        
        # break
        

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