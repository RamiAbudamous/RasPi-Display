import urllib.request
from PIL import Image
import numpy as np

# size to resize image to
SIZE = 238

imageURL = "https://i.scdn.co/image/ab67616d00001e024718e2b124f79258be7bc452"

urllib.request.urlretrieve(imageURL, "image.png")

img = Image.open(r"image.png")
img = img.resize((SIZE, SIZE), Image.Resampling.LANCZOS) # rasPi doesnt have LANCZOS? figure out a different way

array = np.array(img) # convert to bitmap

newIMG = Image.fromarray(array.astype(np.uint8)) # convert from bitmap to PNG

# img.show()
newIMG.show()