#!/usr/bin/env python
# $Id$

# read a list of all files in a directory (sdir)
#  - excludes hidden .files
#  - doesn't recurse into subdirectories
# shuffle list
# copies files with a image_### name into an anon_ directory (adir)
# makes a note of the name mapping in anon_foo.csv (acsv)

import os
import sys
import optparse
import random
import shutil
from subprocess import Popen, PIPE

def main():
    usage = "usage: %prog <directory>"
    parser = optparse.OptionParser(usage)
    (_, args) = parser.parse_args()

    if len(args) == 0:
        parser.error ("No directory specified.")
    elif len(args) > 1:
        parser.error ("Too many arguments.")

    sdir = os.path.abspath(args[0])
    adir = os.path.join(os.path.dirname(sdir), "anon_" + os.path.basename(sdir))
    acsv = os.path.join(os.path.dirname(sdir), "anon_" + os.path.basename(sdir) + ".csv")

    if (not os.path.isdir(sdir)):
        print >>sys.stderr, "Not a directory: '%s'"  % (sdir)
        sys.exit(0)

    if (os.path.isfile(acsv)):
        print >>sys.stderr, "File already exists: '%s'" % (acsv)
        sys.exit(0)

    try:
        os.mkdir(adir)   
    except OSError, ex:
        print >>sys.stderr, "Unable to create directory '%s': %s"  % (adir, ex.strerror)
        sys.exit(0)

    try:
        fh = open(acsv, "w")
    except IOError, ex:
        print >>sys.stderr, "Unable to write file '%s': %s" % (acsv, ex.strerror)
        sys.exit(0)

    filelist = []
    for (_, _, files) in os.walk(sdir):
        files = [f for f in files if not f[0] == '.']
        filelist.extend(files)
        break

    random.shuffle(filelist)

    print >>sys.stdout, "Source directory: %s" % sdir
    print >>sys.stdout, "Target directory: %s" % adir
    print >>sys.stdout, "Mapping file: %s" % acsv

    for s in range(len(filelist)):
        sys.stdout.write('.')
        sfile = filelist[s]
        tfile = "image_%04d%s" % (s + 1, os.path.splitext(sfile)[1])
        fh.write ("%s,%s\n" % (sfile, tfile))
        shutil.copyfile (os.path.join(sdir, sfile), os.path.join(adir, tfile))

    print >>sys.stdout, "done."

    fh.close()
    sys.exit(0)

def osascript(scpt, args=[]):
    p = Popen(['osascript', '-'] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(scpt)
    return stdout

#Example of how to run it.
#osascript("""tell application "System Events" to keystroke "m" using {command down}""")

#Example of how to run with args.
#osascript('''
#    on run {x, y}
#        return x + y
#    end run''', ['2', '2'])

if __name__ == "__main__":
    main()

