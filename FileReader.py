import json

filePath = 'C:\TREC_Washington_Post_collection.v2.jl'

f =open(filePath,'r', encoding='UTF-8')
for line in f:
    article = json.loads(line)
    break
