#!/usr/bin/env python2
__author__ = 'rp'
import sys
import os
import argparse
import shutil
import ConfigParser as configparser
from mutagen.easyid3 import EasyID3

#defaultformat = "{tracknumber}-{artist}-{album}-{title}.{ext}"
defaultformat = "{artist}/{album}/{tracknumber:02d}-{artist}-{title}.{ext}"
supportedextensions = ['mp3', 'ogg']


def id3todict(id3):
    def get(d, k):
        return "" if len(d[k]) == 0 else d[k][0]

    data = dict()
    data['artist'] = get(id3, 'artist')
    data['album'] = get(id3, 'album')
    data['title'] = get(id3, 'title')
    data['date'] = get(id3, 'date')
    data['year'] = data['date'][:4]
    data['tracknumber'] = int(get(id3, 'tracknumber').split('/')[0])
    return data


def renamefiles(args):
    drystr = "[dry]" if args.dry else ""

    if args.recursive:
        print('rec')
    else:
        filelist = [x for x in os.listdir(args.in_dir)
                    if os.path.splitext(x)[1][1:] in supportedextensions]
        for mfile in filelist:
            origpath = os.path.join(args.in_dir, mfile)
            d = id3todict(EasyID3(origpath))
            d['ext'] = os.path.splitext(x)[1][1:]
            newpath = os.path.join(args.out_dir, args.format.format(**d))
            if not 'ext' in args.format:
                newpath += '.' + d['ext']
            try:
                os.makedirs(os.path.dirname(newpath))
            except OSError as err:
                if err.errno != 17:
                    raise err
            if not args.dry:
                shutil.move(origpath, newpath)
            print("{dry}moved: {path}".format(dry=drystr, path=newpath))


def main():
    parser = argparse.ArgumentParser(description="Music file renamer based on tags")
    parser.add_argument('-f', '--format', help="formatting string to use")
    parser.add_argument('-r', '--recursive', action="store_true", help="look recursive in in_dir")
    parser.add_argument('-d', '--dry', action="store_true", help="don't actually copy anything, just show")
    parser.add_argument('in_dir', help="search dir for music files")
    parser.add_argument('out_dir', help="output base directory")

    args = parser.parse_args()

    # load config
    configpath = os.path.expanduser('~/.config/qmmv/config')
    if os.path.exists(configpath):
        cp = configparser.ConfigParser({'format': defaultformat})
        cp.read(configpath)
        if not args.format:
            args.format = cp.get('default', 'format')
    else:
        args.format = defaultformat

    renamefiles(args)
    return 0

if __name__ == "__main__":
    sys.exit(main())
