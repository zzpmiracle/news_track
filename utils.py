import csv

from elasticsearch import Elasticsearch
import json
import re
import time
from bs4 import BeautifulSoup
import codecs
import re
import numpy as np

base_dir = '/home/trec7/zzp/'
def process_doc(doc):
    if not doc['title']:
        return doc['contents']
    doc_string = doc['title']+'.'+doc['contents']
    doc_string = doc_string.replace('\n','').replace('\t','')
    return doc_string

def add_to_es():
    # es = Elasticsearch('localhost:9200')
    mapping ={
    "settings": {
    "analysis" : {
                "analyzer" : {
                    "my_analyzer" : {
                        "tokenizer" : "standard",
                        "filter" : ["standard", "lowercase", "my_stemmer","my_stop"]
                    }
                },
                "filter" : {
                    "my_stemmer" : {
                        "type" : "stemmer",
                        "name" : "english"
                    },
                    "my_stop":{
                        "type":"stop",
                         "stopwords":"_english_"
                    }
                }
            }},
      "mappings": {

          "properties" : {
            "title" : {
              "type" :    "text",
              "analyzer": "my_analyzer"
            },
            "author" : {
                "type" :   "keyword"

            },
            "contents" : {
              "type" :    "text",
              "analyzer": "my_analyzer"
            },
            "kicker" : {
                "type" :   "keyword"
            }
          }
        }

    }
    # result = es.indices.create(index='news',body=mapping,ignore=[400,404])
    # print(result)
    start = time.time()
    sourse_file_Path = base_dir + 'data/TREC_Washington_Post_collection.v2.jl'
    # dst_file_path = 'D:\TREC.txt'
    #match html code
    reg = re.compile('<[^>]*>')
    # es = Elasticsearch()

    articles = {}
    num = 0
    # irrelevant kicker according to GuideLines
    # irrelevant_kicker = ["Opinion", "Letters to the Editor","The Post's View"]

    with open(sourse_file_Path,encoding='UTF-8') as sf:
        for line in sf :
            article = json.loads(line)
            # remove 'type','source'
            # article.pop('type',None)
            # article.pop('source',None)
            # article.pop('article_url')
            # article.pop('published_date')

            id = article['id']
            # article.pop('id')
            paragraph = []
            for content in article['contents']:
                # few contents are None
                if content is not None:
                    # paragraphs
                    if content.get('subtype',None) =='paragraph':
                        if content.get('mime',None) == 'text/plain':
                            # plain text add to list directly
                            paragraph.append(content['content'])
                        elif content.get('mime',None) == 'text/html':
                            # remove html style
                            paragraph.append(re.sub(reg,'',content['content']))
                    # kicker,not sure useful
                    elif content.get('type',None)=='kicker':
                            article['kicker'] = content['content']
            # remove irrelevant articles
            # if article.get('kicker',None) in irrelevant_kicker:
            #     continue
            # transform paragraph list to long string
            article['contents'] = ''.join(paragraph)
            # record number of remain articles
            # result = es.index(index='news',body=article,id=id)
            articles[id] = process_doc(article)
            num += 1
            if num % 10000 == 0:
                print('{} docs completed'.format(num))
    with open(base_dir + 'data/articles.txt','w',encoding='UTF-8') as dic_file:
        dic_file.write(json.dumps(articles))
    print('{} docs remained'.format(num))
    end = time.time()
    print('{:.1f}s'.format(end-start))


def get_topics(filename='D:\\news_track\\newsir18-topics.txt',topic_tag = 'top',num_tag='num',id_tag='docid'):
    soup = BeautifulSoup(codecs.open(filename, "r"), "lxml")
    dic = {}
    for topic in soup.findAll(topic_tag):
        num_str = topic.find(num_tag).getText()
        num = int(re.findall(r'\d+',num_str)[0])
        id = topic.findNext(id_tag).text
        dic[num] = id
    return dic


def id_file():
    sourse_file_Path = 'C:\TREC_Washington_Post_collection.v2.jl'
    id_file = 'G:\\news_track\\ids.csv'
    ids = []
    with open(sourse_file_Path, encoding='UTF-8') as sf,open(id_file,'w',encoding='UTF-8',newline ='') as idfile:
        for line in sf :
            article = json.loads(line)
            ids.append(article['id'])
        ids = [ids]
        id_writer = csv.writer(idfile)
        id_writer.writerows(ids)
add_to_es()