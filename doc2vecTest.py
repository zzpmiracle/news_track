import gensim
# from gensim.models import Doc2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
import re
import json
file_path = 'D:\TREC.txt'

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
            # contents = re.sub(pattern=patten,repl=' ',string=contents)
            contents = re.split(r'\W+', contents)
            print(contents)
            id = article['id']
            documents = TaggedDocument(contents,id)
            yield documents


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
                documents = TaggedDocument(article['contents'], article['id'])
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

docs_generator = text_Generator(file_path)
docs_iterator = [x for x in docs_generator]
# docs_iterator = text_iterator(file_path)
fname = 'vectors.kv'
model = Doc2Vec(documents=docs_iterator,vector_size=100,window=10,min_count=2)
model.save(fname)
