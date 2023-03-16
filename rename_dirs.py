#!/usr/bin/env python3

import argparse
import os
import os.path
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('dir')
parser.add_argument('--separator', default='-')
args = parser.parse_args()

done = set()
for subdir in os.listdir(args.dir):
    old_path = os.path.join(args.dir, subdir)
    if not os.path.isdir(old_path):
        continue
    try:
        i = subdir.index(args.separator)
    except ValueError:
        continue
    new_name = subdir[:i]
    if new_name in done:
        shutil.rmtree(old_path)
    else:
        os.rename(old_path, os.path.join(args.dir, new_name))
        done.add(new_name)
