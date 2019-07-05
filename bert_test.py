import csv
import random

from elasticsearch import Elasticsearch
import json
from utils import get_topics
import numpy

def process_doc(doc):
    if not doc['title']:
        return doc['contents']
    doc_string = doc['title']+'.'+doc['contents']
    doc_string = doc_string.replace('\n','').replace('\t','')
    return doc_string

def create_dataset():
    doc_dic = get_topics()
    data_dir = 'G:\\news_track\\'
    gains_file = data_dir+'bqrels.exp-gains.txt'
    ids_file = data_dir+ 'ids.csv'
    dst_file_path = data_dir+'data.txt'
    es = Elasticsearch()
    # es = Elasticsearch('222.20.24.230:9200')
    ids = set()
    map_file = 'map.txt'

    with open(gains_file) as gf,open(dst_file_path,'a',encoding='utf-8') as df,open(ids_file,'r') as idf:
        gf_reader = csv.reader(gf, delimiter=" ")
        ids_reader = csv.reader(idf)

        ids = next(ids_reader)
        lines = []
        id2s = set()
        for line in gf_reader:
            id1 = doc_dic[int(line[0])]
            id2 = line[2]
            df.write(','.join([id1, id2, line[-1]])+'\n')
            df.write(','.join([id2, id1, line[-1]]) + '\n')
            id2s.add(id2)
            #每个topic 增加同样多的不相关数据
            id3 = random.choice(ids)
            if id3 not in id2s:
                df.write(','.join([id1, id3, '-1']) + '\n')
                df.write(','.join([id3, id1, '-1']) + '\n')
        '''
        随机选取两个id  相关度-1
        保存到ids 和 articles
        '''
        for i in range(10000):
            id = random.sample(ids,2)
            id1 = id[0]
            id2 = id[1]
            df.write(','.join([id1, id2, '-1']) + '\n')
            df.write(','.join([id2, id1, '-1']) + '\n')


if __name__ == "__main__":
    create_dataset()