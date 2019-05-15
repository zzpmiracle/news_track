from elasticsearch import Elasticsearch
import json

es = Elasticsearch('localhost:9200')

# result = es.indices.create(index='news_track',ignore=[400,404])
# print(result)
source_file_path = 'D:\TREC.txt'
i = 0
with open(source_file_path,'r') as sf:
    for line in sf:
        article = json.loads(line)
        id = article['id']
        article.pop('id')
        result = es.index(index='news_track',body=article,id=id)
        if i%5000 == 0:
            print('{}docs completed'.format(i))
        i += 1