'''
Created on 10/09/2011

@author: dave
'''
from multiprocessing import Pool
import Image

from imageprep import rename
from imageprep import resize

def resize_worker(img_obj, args):
    print img_obj.filename, args
    img = Image.open(img_obj.filename)
    (size, mode, out, base, md5, flat) = args
    new_img = img.resize(size, mode)
    new_img.filename = img.filename
    fn = rename.save_img(new_img, out, base, use_hash=md5, flat=flat)
#    data = (fn, new_img.mode, new_img.size, new_img.tostring())    
    return fn

def work(new_size, img_dir, out, md5, procs, landscape_only=False, flat=False):
    # fill the queue
    tasks = list()
    for img in resize.get_img_objs(img_dir):
        (size, mode) = resize.get_resize_args(new_size, img)
        args = (size, mode, out, img_dir, md5, flat)
        data = (img, args)
        tasks.append(data)
    
    pool = Pool(processes=procs)
    data_results = [pool.apply_async(resize_worker, args=t) for t in tasks]
    imgs = list()
    for payload in data_results:
        fn = payload.get()
        print fn
        imgs.append(fn)
    return imgs
