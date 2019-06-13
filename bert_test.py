import csv
import random

from elasticsearch import Elasticsearch
import json
from get_topics import get_topics
import numpy

def process_doc(doc):
    if not doc['title']:
        return doc['contents']
    doc_string = doc['title']+'.'+doc['contents']
    doc_string = doc_string.replace('\n','').replace('\t','')
    return doc_string

def create_dataset():
    doc_dic = get_topics()
    gains_file = 'D:\\news_track\\bqrels.exp-gains.txt'
    dst_file_path = 'D:\\news_track\\data.txt'
    article_map = 'aticle_map.txt'
    # es = Elasticsearch('localhost:9200')
    es = Elasticsearch('222.20.24.230:9200')
    ids = set()
    with open(gains_file) as gf,open(dst_file_path,'a',encoding='utf-8') as df,open(article_map,'w') as am:
        reader = csv.reader(gf, delimiter=" ")
        lines = []
        for line in reader:
            id1 = doc_dic[int(line[0])]
            id2 = line[2]
            df.write(','.join([id1, id2, line[-1]]))
            ids.add(id1)
            ids.add(id2)
        '''
        随机选取两个id  相关度-1
        保存到ids 和 articles
        '''
        map_file = 'map.txt'
        with open(map_file, 'r') as mf:
            id_map = json.loads(next(mf))
        for i in range(10000):
            id = random.sample(list(id_map.keys()),2)
            id1 = id[0]
            id2 = id[1]
            df.write(','.join([id1, id2, '-1']))
            ids.add(id1)
            ids.add(id1)
        articles = {}
        for id in ids:
            articles['id'] = process_doc(es.get(index='news',id=id)['_source'])
            # lines.append(doc1+','+doc2+','+line[-1])
            # lines.append([doc1,doc2,line[-1]])
        am.write(json.dumps(articles))

if __name__ == "__main__":
    create_dataset()