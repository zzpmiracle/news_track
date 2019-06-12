import csv
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

    # es = Elasticsearch('localhost:9200')
    es = Elasticsearch('222.20.24.230:9200')
    ids = set()
    with open(gains_file) as gf,open(dst_file_path,'w',encoding='utf-8') as df:
        reader = csv.reader(gf, delimiter=" ")
        lines = []
        for line in reader:
            id1 = doc_dic[int(line[0])]
            id2 = line[2]
            df.write(','.join([id1, id2, line[-1]]))
            ids.add(id1)
            ids.add(id2)
        articles = {}
        for id in ids:
            articles['id'] = process_doc(es.get(index='news',id=id)['_source'])
            # lines.append(doc1+','+doc2+','+line[-1])
            # lines.append([doc1,doc2,line[-1]])
'''
随机选取两个id  相关度-1
保存到ids 和 articles
'''

if __name__ == "__main__":
    create_dataset()