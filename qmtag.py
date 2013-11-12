#!/usr/bin/env python2
__author__ = 'rp'
import sys
import os
import argparse

defaultformat = "{trknr}-{artist}-{album}.{ext}"
supportedextensions = ['mp3', 'ogg']


def renamefiles(args):
    if not args.format:
        args.format = defaultformat

    if args.recursive:
        print('rec')
    else:
        filelist = [x for x in os.listdir(args.in_dir)
                    if os.path.splitext(x)[1][1:] in supportedextensions]
        for mfile in filelist:
            print(mfile)
    print(args)


def main():
    parser = argparse.ArgumentParser(description="Music file renamer based on tags")
    parser.add_argument('-f', '--format', help="formatting string to use")
    parser.add_argument('-r', '--recursive', action="store_true", help="look recursive in in_dir")
    parser.add_argument('in_dir', help="search dir for music files")
    parser.add_argument('out_dir', help="output base directory")

    renamefiles(parser.parse_args())
    return 0

if __name__ == "__main__":
    sys.exit(main())
