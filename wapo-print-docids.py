#!/usr/bin/env python3

import argparse
import json
import re
import hashlib
import collections

parser = argparse.ArgumentParser(description='Filter the Washington Post collection to remove exact duplicates.')
parser.add_argument('bundle', nargs='+', help='WaPo bundle(s) to read')

args = parser.parse_args()

# Read bundles and dump docids
for file in args.bundle:
    with open(file, 'r') as f:
        for line in f:
            obj = json.loads(line)
            docid = obj['id']
            print(docid)
