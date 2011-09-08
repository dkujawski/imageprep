'''
Created on 6/09/2011

@author: dave
'''

import Image
import os

def is_landscape(img_obj):
    """ return True if image is wider than it is high
    """
    x, y = img_obj.size
    return x > y

def get_new_y(img_obj, new_x):
    """ based on the desired new x size, return the new y size necessary in 
    order to maintain proper aspect ratio
    """
    old_x, old_y = img_obj.size
    return int(float(new_x) / old_x * old_y)

def get_each_img_obj(img_dir):
    """ walk the img_dir and return each found image as an Image object
    """
    for root, _, files in os.walk(img_dir):
        for fn in files:
            fp = os.path.join(root, fn)
            try:
                img = Image.open(fp)
            except IOError as ioe:
                print ioe, ", skipping:", fp
                continue
            if img.format and is_landscape(img):
                yield img

def get_each_resized_img(new_x, img_dir):
    """ return a resized Image object for each image file found in the img_dir
    """
    filter_mode = Image.ANTIALIAS
    for img in get_each_img_obj(img_dir):
        new_y = get_new_y(img, new_x)
        new_size = (new_x, new_y)
        new_img = img.resize(new_size, filter_mode)
        new_img.filename = img.filename
        yield new_img
        