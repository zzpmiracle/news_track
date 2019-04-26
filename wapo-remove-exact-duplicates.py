#!/usr/bin/env python3

import argparse
import json
import re
import hashlib
import collections

epilog=''' This script retains the last copy of each document in the
dupeslist, and outputs all of those documents at the end.  This means
that the documents in the output bundle will be in a different order
than in the input.  you should run the script over all the bundles at
the same time:

   ./wapo-remove-exact-duplicates.py wapo-docics-dupes WaPo/data/TREC_*txt > wapo-deduped.jl

'wc -l wapo-deduped.jl' should print '595037'.
'''
parser = argparse.ArgumentParser(description='Filter the Washington Post collection to remove exact duplicates.',
                                 epilog = epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('dupeslist', help='List of duplicate document IDs in (count, docid) format')
parser.add_argument('bundle', nargs='+', help='WaPo bundle(s) to read')

args = parser.parse_args()

dupes = {}
with open(args.dupeslist, 'r') as dupefile:
    for line in dupefile:
        (count, docid) = line.split()
        dupes[docid] = count

# Read bundles, holding on to latest version of each known dupe.
for file in args.bundle:
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            obj = json.loads(line)
            docid = obj['id']
            if docid in dupes:
                dupes[docid] = line
                continue
            print(line)

# Now dump the dupes.
for d, line in dupes.items():
    print(line)
