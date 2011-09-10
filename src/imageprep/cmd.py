'''
Created on 6/09/2011

@author: dave
'''
import argparse
import os
import sys

from imageprep import process
from imageprep import rename
from imageprep import resize

DESC = "Commandline tool used for resizing a directory of images."

def is_valid_dir(path_str):
    """ check to see if the path_str exists on the file system and is a
    directory, if not raise an error.
    """
    resolved_path = os.path.abspath(path_str)
    if os.path.exists(resolved_path) and os.path.isdir(resolved_path):
        return resolved_path
    msg = "path is not a directory or does not exist:\n\t%s" % resolved_path
    raise argparse.ArgumentTypeError(msg)

def build_parser():
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('base', nargs='+', type=is_valid_dir, 
                        help='the base directory tree to search')
    parser.add_argument('-w', '--width', type=int, default=640, 
                        help="new width to set for images.")
    parser.add_argument('-o', '--outdir', type=is_valid_dir,
                        default='./', help='output directory for new files')
    parser.add_argument('--md5', action='store_true', default=False,
                        help='use md5 checksum for new file names')
    parser.add_argument('--profile', action='store_true', default=False,
                        help='profile the run')
    parser.add_argument('--faster', action='store_true', default=False,
                        help='go faster')
    parser.add_argument('--procs', nargs='?', type=int, default=2,
                        help='when go faster, set the processes used.')
    return parser

def run(args):
    out = os.path.abspath(args.outdir)
    for base in args.base:        
        print "processing:", base
        count = 0
        if args.faster:
            imgs = process.work(args.width, base, out, args.md5, args.procs)
            count = len(imgs)
        else:
            for img in resize.get_resized_imgs(args.width, base):
                ret = rename.save_img(img, out, use_hash=args.md5)
                print ret
                count += 1
        print "processed %d images." % count
        
if __name__ == '__main__':
    bp = build_parser()
    args = bp.parse_args()
    if not args.base:
        bp.print_help()
        sys.exit(1)
    if args.profile:
        import dkprof
        cmd = "run(args)"
        dkprof.do_profile(cmd)
    else:
        run(args)
    print 'done!'
        