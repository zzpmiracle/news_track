import json
import re
import string
import time
start = time.time()


irrevelant_kicker = ["Opinion", "Letters to the Editor","The Post's View"]
sourse_file_Path = 'C:\TREC.txt'
dst_file_path = 'D:\TREC_v2.txt'


i = 0
after = 0
# file_writer = open(dst_file_path, 'w')

with open(sourse_file_Path,encoding='UTF-8') as sf,open(dst_file_path, 'w') as df:
    for line in sf :
        i+=1
        if i%10000==0:
            print(i)
        article = json.loads(line)
        if article.get('kicker',None) in irrevelant_kicker:
            continue
        after+=1
        paragraph = article['contents']
        paragraph = '\n'.join(paragraph)
        article['contents'] = paragraph
        df.write(json.dumps(article))
        df.write('\n')

end = time.time()
print('before:{},\nafter:{}'.format(i,after))
#before:595037
#after:571963

print('{}s'.format(end-start))
#72.11868238449097s