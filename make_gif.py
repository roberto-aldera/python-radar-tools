import glob
from PIL import Image
import os
import settings


def generate_thumbnails(folder_to_process):
    thumbnail_dimension = 512
    size = thumbnail_dimension, thumbnail_dimension
    images_batch = folder_to_process + "*.jpg"

    for infile in glob.glob(images_batch):
        im = Image.open(infile)
        im.thumbnail(size, Image.ANTIALIAS)
        outfile = os.path.splitext(infile)[0] + ".thumbnail"
        im.save(outfile, "JPEG")


def generate_gif(folder_to_process):
    fp_in = folder_to_process + "*.thumbnail"
    fp_out = folder_to_process + "image.gif"

    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=50, loop=0)


if __name__ == "__main__":
    folder_containing_images = settings.ROOT_DIR + "Vehicle-ahead/"
    generate_thumbnails(folder_containing_images)
    generate_gif(folder_containing_images)
