import json
import re
import string
import time
start = time.time()
from elasticsearch import Elasticsearch
sourse_file_Path = 'D:\TREC_Washington_Post_collection.v2.jl'
# dst_file_path = 'D:\TREC.txt'
#match html code
reg = re.compile('<[^>]*>')
es = Elasticsearch()

num = 0
# irrelevant kicker according to GuideLines
# irrelevant_kicker = ["Opinion", "Letters to the Editor","The Post's View"]

with open(sourse_file_Path,encoding='UTF-8') as sf:
    for line in sf :
        article = json.loads(line)
        # remove 'type','source'
        article.pop('type',None)
        article.pop('source',None)
        article.pop('article_url')
        article.pop('published_date')

        id = article['id']
        article.pop('id')
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
        result = es.index(index='news_track',body=article,id=id)
        num += 1
        if num % 10000 == 0:
            print('{} docs completed'.format(num))
print('{} docs remained'.format(num))
end = time.time()
print('{:.1f}s'.format(end-start))