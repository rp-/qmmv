#!/usr/bin/env python2
__author__ = 'rp'
import sys
import os
import argparse
import shutil
import ConfigParser as configparser
import mutagen

#defaultformat = "{tracknumber}-{artist}-{album}-{title}.{ext}"
defaultformat = "{artist}/{album}/{tracknumber:02d}-{artist}-{title}.{ext}"
supportedextensions = ['mp3', 'ogg', 'm4a']


def tagdatatodict(tagdata):
    def get(d, k):
        return "" if len(d[k]) == 0 else d[k][0]

    def gettrknr(val):
        if isinstance(val, tuple):
            return val[0]
        return int(val.split('/')[0])

    data = dict()
    keys = {'artist': 'artist', 'album': 'album',
            'title': 'title', 'date': 'date',
            'tracknumber': 'tracknumber'}

#    print(tagdata, type(tagdata))
    data['artist'] = get(tagdata, 'artist')
    data['album'] = get(tagdata, 'album')
    data['title'] = get(tagdata, 'title')
    data['date'] = get(tagdata, 'date')
    data['year'] = data['date'][:4]
    data['tracknumber'] = gettrknr(get(tagdata, 'tracknumber'))
    #print(data)
    return data


def renamefiles(args):
    drystr = "[dry]" if args.dry else ""

    filelist = list()
    if args.recursive:
        print('rec')

    filelist = [x for x in os.listdir(args.in_dir)
                if os.path.splitext(x)[1][1:] in supportedextensions]
    for mfile in filelist:
        origpath = os.path.join(args.in_dir, mfile)
        d = tagdatatodict(mutagen.File(origpath, easy=True))
        d['ext'] = os.path.splitext(mfile)[1][1:]
        newpath = os.path.join(args.out_dir, args.format.format(**d))
        if not 'ext' in args.format:
            newpath += '.' + d['ext']

        if not args.dry:
            try:
                os.makedirs(os.path.dirname(newpath))
            except OSError as err:
                if err.errno != 17:
                    raise err
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
