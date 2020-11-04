import sys
import numpy as np
from PIL import Image, ImageOps
import time
from pathlib import Path
import shutil
from argparse import ArgumentParser
import settings
import pdb

sys.path.insert(-1, "/workspace/code/corelibs/src/tools-python")
sys.path.insert(-1, "/workspace/code/corelibs/build/datatypes")
sys.path.insert(-1, "/workspace/code/radar-utilities/build/radarutilities_datatypes_python")
sys.path.insert(-1, "/workspace/code/corelibs/src/tools-python/mrg/adaptors")


def export_radar_images(params):
    subset_start_index = params.subset_start_index
    num_samples = params.num_samples
    skip_every_nth_frame = params.skip_every_nth_frame
    image_dimension = params.image_dimension
    sensor_rotation = params.rotation_angle
    output_file_extension = params.output_file_extension
    intensity_multiplier = 2

    print("Generating data, size =", num_samples)
    from mrg.logging.indexed_monolithic import IndexedMonolithic
    from mrg.adaptors.radar import pbNavtechRawConfigToPython, pbNavtechRawScanToPython

    split_data_path = Path(settings.RADAR_IMAGE_DIR)
    if split_data_path.exists() and split_data_path.is_dir():
        shutil.rmtree(split_data_path)
    split_data_path.mkdir(parents=True)

    radar_config_mono = IndexedMonolithic(settings.RADAR_CONFIG)
    config_pb, name, timestamp = radar_config_mono[0]
    config = pbNavtechRawConfigToPython(config_pb)
    radar_mono = IndexedMonolithic(settings.RAW_SCAN_MONOLITHIC)
    # pdb.set_trace()
    # radar_mono_to_process = radar_mono[subset_start_index:subset_start_index + num_samples]

    for i in range(num_samples):
        if i % skip_every_nth_frame == 0:
            scan_index = subset_start_index + i
            pb_raw_scan, name_scan, _ = radar_mono[scan_index]
            radar_sweep = pbNavtechRawScanToPython(pb_raw_scan, config)

            width, height, res = (image_dimension,
                                  image_dimension,
                                  config.bin_size_or_resolution)
            cart_img = radar_sweep.GetCartesian(pixel_width=width, pixel_height=height, resolution=res,
                                                method='cv2', verbose=False)
            img = Image.fromarray(cart_img.astype(np.uint8) * intensity_multiplier, 'L')
            img = img.rotate(sensor_rotation)
            img = ImageOps.mirror(img)
            # pdb.set_trace()

            img.save("%s%s%i%s" % (split_data_path, "/", scan_index, output_file_extension))
            img.close()
            if i % 5 == 0:
                print("Completed image generation for images:", i)

    print("Generated samples up to index:", scan_index, "with dim =", image_dimension,
          "and written to:", split_data_path)


def main():
    # Define a main loop to run and show some example data if this script is run as main
    parser = ArgumentParser(add_help=False)
    parser.add_argument('--subset_start_index', type=int, default=0, help='Scan index from which to begin processing')
    parser.add_argument('--num_samples', type=int, default=10, help='Number of samples for processing')
    parser.add_argument('--skip_every_nth_frame', type=int, default=1, help='Number of samples for processing')
    parser.add_argument('--image_dimension', type=int, default=settings.RADAR_IMAGE_DIMENSION,
                        help='Size of scan to consider in exported image')
    parser.add_argument('--rotation_angle', type=int, default=180, help='Account for sensor offset angle')
    parser.add_argument('--output_file_extension', type=str, default=".jpg", help='File extension for output images')

    params = parser.parse_args()
    print("Starting dataset generation...")
    start_time = time.time()

    export_radar_images(params)
    print("--- Radar image generation execution time: %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
