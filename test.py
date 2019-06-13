import json
import random

map_file = 'map.txt'
with open(map_file, 'r') as mf:
    id_map = json.loads(next(mf))

print(random.sample(id_map.keys(),2))