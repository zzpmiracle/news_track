import csv
from elasticsearch import Elasticsearch
import json
from get_topics import get_topics

def process_doc(doc):
    doc_string = doc['title']+'.'+doc['contents']
    doc_string = doc_string.replace('\n','').replace('\t','')
    return doc_string
def create_dataset():
    doc_dic = get_topics()
    gains_file = 'D:\\news_track\\bqrels.exp-gains.txt'
    # es = Elasticsearch('localhost:9200')
    es = Elasticsearch('222.20.24.230:9200')
    with open(gains_file) as gf:
        reader = csv.reader(gf, delimiter=" ")
        lines = []
        for line in reader:
            id1 = doc_dic[int(line[0])]
            id2 = line[2]
            doc1 = es.get(index='news', id=id1)['_source']
            doc2 = es.get(index='news', id=id2)['_source']
            doc1 = process_doc(doc1)
            doc2 = process_doc(doc2)
            lines.append(doc1+'\t'+doc2+'\t'+line[-1])
    print(lines)
if __name__ == "__main__":
    create_dataset()