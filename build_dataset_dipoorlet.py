# build data for dipoorlet
# data need to satisfy certain naming format 

import os
import random
from PIL import Image
from calibrator import get_calib_data_path, Preprocess

random.seed(43)

def get_dipoorlet_calib():
    data_root = "tiny-imagenet-200/val/images/"
    to_root = "cali_data_2pics/input.1/"
    if not os.path.exists(to_root):
        os.makedirs(to_root)
    image_list = get_calib_data_path()    

    for i, image_path in enumerate(image_list):
        image = Image.open(data_root + image_path).convert("RGB")
        image = Preprocess(image).numpy()
        image.tofile(to_root + str(i) + ".bin")


get_dipoorlet_calib()