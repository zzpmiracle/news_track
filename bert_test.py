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
    dst_file_path = 'data.txt'
    article_map = 'article_map.txt'
    es = Elasticsearch('localhost:9200')
    # es = Elasticsearch('222.20.24.230:9200')
    ids = set()
    map_file = 'map.txt'

    with open(gains_file) as gf,open(dst_file_path,'a',encoding='utf-8') as df,open(article_map,'w') as am,open(map_file, 'r') as mf:
        reader = csv.reader(gf, delimiter=" ")
        id_map = list(json.loads(next(mf)).keys())
        lines = []
        for line in reader:
            id1 = doc_dic[int(line[0])]
            id2 = line[2]
            if id1 in id_map and id2 in id_map:
                df.write(','.join([id1, id2, line[-1]])+'\n')
                ids.add(id1)
                ids.add(id2)
            #每个topic 增加同样多的
            id3 = random.choice(id_map)
            if id3 not in ids:
                df.write(','.join([id1, id3, '-1']) + '\n')
                ids.add(id3)
        '''
        随机选取两个id  相关度-1
        保存到ids 和 articles
        '''
        for i in range(10000):
            id = random.sample(id_map,2)
            id1 = id[0]
            id2 = id[1]
            df.write(','.join([id1, id2, '-1'])+'\n')
            ids.add(id1)
            ids.add(id1)
        articles = {}
        for id in ids:
            articles[id] = process_doc(es.get(index='news',id=id)['_source'])
            # lines.append(doc1+','+doc2+','+line[-1])
            # lines.append([doc1,doc2,line[-1]])
        am.write(json.dumps(articles))

if __name__ == "__main__":
    create_dataset()