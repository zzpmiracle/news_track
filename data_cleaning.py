import json
import re
import string
import time
start = time.time()

sourse_file_Path = 'C:\TREC_Washington_Post_collection.v2.jl'
dst_file_path = 'D:\TREC.txt'
#match html code
reg = re.compile('<[^>]*>')

num = 0
#irrelevant kicker according to GuideLines
irrevelant_kicker = ["Opinion", "Letters to the Editor","The Post's View"]

with open(sourse_file_Path,encoding='UTF-8') as sf,open(dst_file_path, 'w') as df:
    for line in sf :
        article = json.loads(line)
        #remove 'type','sourse'
        article.pop('type',None)
        article.pop('source',None)
        paragraph = []
        for content in article['contents']:
            #few contents are None
            if content is not None:
                # paragraphs
                if content.get('subtype',None) =='paragraph':
                    if content.get('mime',None) == 'text/plain':
                        #plain text add to list directly
                        paragraph.append(content['content'])
                    elif content.get('mime',None) == 'text/html':
                        #remove html style
                        paragraph.append(re.sub(reg,'',content['content']))
                #kicker,not sure useful
                elif content.get('type',None)=='kicker':
                        article['kicker'] = content['content']
        #remove irrelevant articles
        if article.get('kicker',None) in irrevelant_kicker:
            continue
        #transform paragraph list to long string
        article['contents'] = '\n'.join(paragraph)
        #write article to file
        df.write(json.dumps(article))
        df.write('\n')
        #record number of remain articles
        num += 1
        if num % 10000 == 0:
            print('{} docs completed'.format(num))#
print('{} docs remained'.format(num))
end = time.time()
print('{:.1f}s'.format(end-start))