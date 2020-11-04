import glob
from PIL import Image
import os
import settings

thumbnail_dimension = 256
size = thumbnail_dimension, thumbnail_dimension
images_folder = settings.ROOT_DIR + "T-junction/"
images_batch = images_folder + "*.png"

for infile in glob.glob(images_batch):
    im = Image.open(infile)
    im.thumbnail(size, Image.ANTIALIAS)
    outfile = os.path.splitext(infile)[0] + ".thumbnail"
    im.save(outfile, "JPEG")
