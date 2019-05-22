from elasticsearch import Elasticsearch
import json

es = Elasticsearch('localhost:9200')
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
# result = es.indices.create(index='news_track',ignore=[400,404])
# print(result)
source_file_path = 'D:\TREC.txt'
i = 0
with open(source_file_path,'r') as sf:
    for line in sf:
        article = json.loads(line)
        id = article['id']
        article.pop('id')
        article.pop('article_url')
        article.pop('published_date')
        result = es.index(index='news',body=article,id=id)
        if i%5000 == 0:
            print('{}docs completed'.format(i))
        i += 1