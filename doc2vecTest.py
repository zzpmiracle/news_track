import gensim
# from gensim.models import Doc2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
import re
import json
file_path = 'D:\TREC.txt'
import time
start = time.time()
def text_Generator(file_path):
    with open(file_path,'r') as file:
        count = 0
        for line in file:
            count+=1
            article = json.loads(line)
            contents = article['contents']
            contents = re.sub('\n','',contents)
            # print(contents)
            # patten = "[.!//_,$&%^*()<>+\"'?@#-|:~{}]+"

            patten = "[\.!//_,$&%^*()<>+\"'?@#-|:~{}]+|[——！\\\\，。=？、：“”‘’《》【】￥……（）]+"
            punc = '[,.!\'"?$@]'

            contents = re.sub(pattern=punc,repl='',string=contents)
            # contents = re.split(r3, contents)
            # print(contents)
            id = article['id']
            documents = TaggedDocument(contents,[str(id)])
            if count<1000:
                yield documents
            else:
                break


class text_iterator():
    def __init__(self,filepath):
        self.filepath = filepath
        self.docs = self.text_Generator()

    def text_Generator(self):
        with open(self.filepath, 'r') as file:
            count = 0
            for line in file:
                count += 1
                article = json.loads(line)
                documents = TaggedDocument(article['contents'], [article['id']])
                if count <= 10000:
                    yield documents
                else:
                    break

    def __iter__(self):
        return self
    def __next__(self):
        doc = next(self.docs)
        if doc is not None:
            return doc
        else:
            raise StopIteration

docs = []
id_map = {}
with open(file_path,'r') as file:
    count = 0
    for line in file:

        article = json.loads(line)
        contents = article['contents']
        contents = re.sub('\n','',contents)
        # print(contents)
        # patten = "[.!//_,$&%^*()<>+\"'?@#-|:~{}]+"
        patten = "[\.!//_,$&%^*()<>+\"'?@#-|:~{}]+|[——！\\\\，。=？、：“”‘’《》【】￥……（）]+"
        punc = '[,.!\'"?$@]'
        contents = re.sub(pattern=punc,repl='',string=contents)
        # contents = re.split(r3, contents)
        # print(contents)
        id = article['id']
        id_map[id] = count
        document = TaggedDocument(contents,[str(id)])
        docs.append(document)
        count += 1
map_file = 'map.txt'
with open(map_file,'w') as mf:
    mf.write(json.dumps(id_map))
# docs_generator = text_Generator(file_path)
# docs_iterator = [x for x in docs_generator]

fname = 'vectors.kv'
model = Doc2Vec(documents=docs,vector_size=100,window=10,min_count=2,workers=10)
model.save(fname)
end = time.time()
print('{:.1f}s'.format(end-start))