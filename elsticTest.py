from elasticsearch import Elasticsearch
es = Elasticsearch('222.20.25.124:9200')
from get_topics import get_topics
topics = get_topics()
index = 'news_track'
#get topics as a dic
for num,id in topics.items():
    article = es.get(index=index,id=id)['_source']
    print(article)
    break
    #each topic's num and id
result = es.search(index,_source_includes=['contents.keyword'])
print(result)

from RAKE.rake import Rake
rake = Rake()
