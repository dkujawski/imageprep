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

def get_new_x(img_obj, new_y):
    """ based on the desired new x size, return the new y size necessary in 
    order to maintain proper aspect ratio
    """
    old_x, old_y = img_obj.size
    return int(float(new_y) / old_y * old_x)

def get_img_objs(img_dir, landscape_only=False):
    """ walk the img_dir and build Image objects out of any images found
    """
    for root, _, files in os.walk(img_dir):
        for fn in files:
            fp = os.path.join(root, fn)
            try:
                img = Image.open(fp)
            except IOError as ioe:
                print ioe, ", skipping:", fp
                continue
            if img.format:
                if landscape_only:
                    if is_landscape(img):
                        yield img
                    else:
                        continue
                else:
                    yield img

def get_resized_imgs(new_x, img_dir, landscape_only=False):
    """ return list of resized Image objects for each image file found in the 
    img_dir
    """
    for img in get_img_objs(img_dir, landscape_only):
        args = get_resize_args(new_x, img)
        # this is slow....
        new_img = img.resize(*args)
        new_img.filename = img.filename
        yield new_img
        
def get_resize_args(max_size, img):
    filter_mode = Image.ANTIALIAS
    (x,y) = img.size
    if x > y: 
        new_y = get_new_y(img, max_size)
        new_x = max_size
    else:
        new_y = max_size
        new_x = get_new_x(img, max_size)
    new_size = (new_x, new_y)
    return (new_size, filter_mode,)
