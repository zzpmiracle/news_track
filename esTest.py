from elasticsearch import Elasticsearch
import json

es = Elasticsearch('http://104.248.219.97:9200')

# result = es.indices.create(index='news_track',ignore=[400,404])
# print(result)
sourse_file_path = 'D:\TREC_v2.txt'
i = 0
with open(sourse_file_path,'r') as sf:
    while i<100000:
        article = json.loads(next(sf))
        result = es.index(index='news_track',body=article)
        if i%5000 == 0:
            print('{}docs completed'.format(i))
        i+=1