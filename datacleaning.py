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
# file_writer = open(dst_file_path, 'w')

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
                        paragraph.append(content['content'])
                    elif content.get('mime',None) == 'text/html':
                        paragraph.append(re.sub(reg,'',content['content']))
                #kicker,not sure useful
                elif content.get('type',None)=='kicker':
                        article['kicker'] = content['content']
        article['contents'] = paragraph
        df.write(json.dumps(article))
        df.write('\n')
        num += 1
        if num % 10000 == 0:
            print('{} docs completed'.format(num))

end = time.time()
print('{:.1f}s'.format(end-start))