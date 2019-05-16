from gensim.models.doc2vec import Doc2Vec, TaggedDocument
fname = 'vectors.kv'
model = Doc2Vec.load(fname)
print(model.docvecs.most_similar(998))

from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from get_topics import get_topics
import json
fname = 'vectors.kv'
map_file = 'map.txt'
topics = get_topics()
model = Doc2Vec.load(fname)

with open(map_file,'r') as mf:
    id_map = json.loads(next(mf))
for num,search_id in topics.items():
    doc_id = id_map[search_id]
    print(model.docvecs.most_similar(doc_id,topn=100))
