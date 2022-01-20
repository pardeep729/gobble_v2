import os
import time

from fpdf import FPDF

# A4 page size, mm
PAGE_W = 210
PAGE_H = 297
PAGE_SIZE = (PAGE_W, PAGE_H)

CARD_D = 85 # Card diamter on page, mm
CARDS_PER_ROW = 2 # Number of cards on the same row on the page
CARDS_PER_COL = 3 # Number of cards on the same column on the page
CARDS_PER_PAGE = CARDS_PER_ROW*CARDS_PER_COL # Number of cards on a page
GAP_BETWEEN_CARDS = 5 # Gap between cards on grid, mm

# The max size of the content area
CONTENT_W = CARDS_PER_ROW*CARD_D + (CARDS_PER_ROW - 1)*GAP_BETWEEN_CARDS
CONTENT_H = CARDS_PER_COL*CARD_D + (CARDS_PER_COL - 1)*GAP_BETWEEN_CARDS

# Where to start placing images from, so that it all gets centred
X_STARTING = (PAGE_W-CONTENT_W)/2
Y_STARTING = (PAGE_H-CONTENT_H)/2

CARD_FOLDER_NAME = 'export' # Name of folder containing card images (generated from gobble)
CARD_BACK_FOLDER_NAME = 'static_images'
CARD_BACK_FILENAME = 'card_back.png'

OUTPUT_FOLDER_NAME = 'printable'
OUTPUT_FILENAME = 'gobble_cards.pdf'

def gobble_to_pdf():
    # Check that an export folder exists
    OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), OUTPUT_FOLDER_NAME)
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER) 
    
    # Create pdf instance
    pdf = FPDF(orientation='P', unit='mm', format=PAGE_SIZE)

    # Grab all necessary images
    images_dirname_rel = CARD_FOLDER_NAME
    images_dirname_abs = os.path.join(os.path.dirname(__file__), CARD_FOLDER_NAME)
    image_filenames = os.listdir(images_dirname_abs)
    image_fps = [os.path.join(images_dirname_abs, fn) for fn in image_filenames]

    card_back_fp = os.path.join(os.path.dirname(__file__), CARD_BACK_FOLDER_NAME, CARD_BACK_FILENAME) # Get card back

    # Create relevant pages in batches of 6. If the final group is less than 6, create a page of that many cards.
    remaining = len(image_fps) # Number of cards to be placed on a page for printing
    curr_pos = 0 # Keep track of where to start in the list of card images for each loop
    while remaining > 0: # Keep looping while there are cards to be placed
        image_fps_for_grid = image_fps[curr_pos:curr_pos+CARDS_PER_PAGE]
        image_fns_for_grid = image_filenames[curr_pos:curr_pos+CARDS_PER_PAGE]
        card_back_fps_for_grid = [card_back_fp for _ in range(len(image_fps_for_grid))]

        add_page_and_populate(pdf, image_fps_for_grid, image_fns_for_grid) # Generate card fronts
        add_page_and_populate(pdf, card_back_fps_for_grid) # Generate card backs

        remaining -= len(image_fps_for_grid) # Decrement remaining counter each loop
        curr_pos += CARDS_PER_PAGE # Increment current position, so start at right place in next loop

    # Output to file
    pdf.output(os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME), 'F')

def add_page_and_populate(pdf: FPDF, image_filepaths: list, image_filenames=None):
    """
    TODO: doc string
    """

    pdf.add_page() # Create new page

    i = 0 # Go through list of image file paths one-by-one

    for row in range(CARDS_PER_COL):
        for col in range(CARDS_PER_ROW):
            x_pos = X_STARTING + col*(CARD_D + GAP_BETWEEN_CARDS) 
            y_pos = Y_STARTING + row*(CARD_D + GAP_BETWEEN_CARDS)

            try:
                pdf.image(image_filepaths[i], w=CARD_D, h=CARD_D, x=x_pos, y=y_pos) # Place image on page
                if image_filenames is not None:
                    pdf.set_xy(x_pos, y_pos)
                    pdf.set_font('Arial', 'B', 8)
                    pdf.set_text_color(0,0,0)
                    pdf.write(5, f"{image_filenames[i]}")
                # print(f"{i} Card placed at row {row} col {col}, position x={x_pos}mm y={y_pos}mm.") # Print a helpful message
                i += 1 # Iterate counter, so can get next image on next lop
            except IndexError as e:
                print(f"{i} No more cards, so will break loop early")
                return
    
###################
# App starts here #
###################
if __name__ == '__main__':
    start = time.time()
    gobble_to_pdf()
    end = time.time()
    print(f"Program took {end - start} seconds to run.")