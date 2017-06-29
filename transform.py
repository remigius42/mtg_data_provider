"""Generate rotated images for all images."""

import glob
import warnings
import download
import numpy as np
import skimage.io
import skimage.transform
from joblib import Parallel, delayed

MAX_WIDTH = 400
MAX_HEIGHT = 400

def _get_rotated_image_path(image_path, rotation):
    """Determines the path to store the rotated image."""
    return image_path.split("_base.jpg")[0] + "_" + str(rotation) + ".jpg"

def _generate_images(image_path, rotations):
    """Generate rotated images of a given image."""
    image = skimage.io.imread(image_path)
    for angle in rotations:
        rotated_image = skimage.img_as_ubyte(
            skimage.transform.rotate(image, angle, resize=True))
        new_image = np.zeros((MAX_WIDTH, MAX_HEIGHT, 3), dtype=np.uint8)
        x_offset = (MAX_WIDTH - rotated_image.shape[0]) // 2
        y_offset = (MAX_HEIGHT - rotated_image.shape[1]) // 2
        new_image[x_offset:(x_offset + rotated_image.shape[0]),
                  y_offset:(y_offset + rotated_image.shape[1])] = rotated_image
        skimage.io.imsave(_get_rotated_image_path(image_path, angle), new_image)

def _get_all_base_images(images_path):
    """Get all base image paths for given images folder."""
    return glob.glob(images_path + "/**/*_base.jpg")

def rotate_images(images_path):
    """Generate rotated images of all base images."""
    base_images = _get_all_base_images(images_path)
    rotations = range(0, 360, 45)
    Parallel(n_jobs=-2)(delayed(_generate_images)(image_path, rotations)
                        for image_path in base_images)

if __name__ == '__main__':
    warnings.filterwarnings("ignore", "Possible precision loss.*")
    IMAGES_PATH = download.DEFAULT_OUTPUT_PATH
    rotate_images(IMAGES_PATH)
