import random
import math

# arrangements = ['a', 'b', 'c']
# results = [random.randint(0,len(arrangements)-1) for _ in range(10000)]

# print(max(results), min(results), sum(results)/len(results))


from PIL import Image

image = Image.open('static_images\card_back.PNG') # Load source image
imageBox = image.getbbox() # Get box around content
cropped = image.crop(imageBox) # Crop to content
cropped.save('static_images\card_back_cropped.PNG') # Output cropped image to target directory