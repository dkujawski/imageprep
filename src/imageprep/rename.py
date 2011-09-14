'''
Created on 6/09/2011

@author: dave
'''
import hashlib
import os

def get_hash_key(data):
    """ generate a hash key using data
    """
    md5 = hashlib.md5()
    md5.update(data)
    key = md5.hexdigest()
    return key

def get_new_filename(img_obj):
    """ return a new filename for the image based on a hash of the new image 
    data. 
    """
    data = img_obj.tostring()
    _, ext = os.path.splitext(img_obj.filename)
    return "%s%s" % (get_hash_key(data), ext)

def save_img(img_obj, out_dir, base, use_hash=False, flat=False):
        """ save the image file into the out_dir, if use_hash=True generate a
        hash based on the img_obj data and use that for the file name.
        """
        if use_hash:
            fn = get_new_filename(img_obj)
        else:
            fn = os.path.basename(img_obj.filename)
        
        if flat:
            new_path = os.path.join(out_dir, fn)
        else:
            sub_dirs = img_obj.filename.replace(base, '').lstrip('/')
            new_base = os.path.dirname(os.path.join(out_dir, sub_dirs))
            if not os.path.exists(new_base):
                os.makedirs(new_base)
            new_path = os.path.join(new_base, fn)
        try:
            img_obj.save(new_path)
        except IOError as ioe:
            """ if the save fails it will raise an IOError. remove the file if
            it was created, we cannot be sure if it is complete.
            """
            if os.path.exists(new_path):
                print ioe, new_path
                os.remove(new_path)
                return
        return new_path
        
    