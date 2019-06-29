from elasticsearch import Elasticsearch
from RAKE.rake import Rake

from get_topics import get_topics


host_ip = '222.20.25.124'
# es = Elasticsearch('222.20.25.124:9200')
es= Elasticsearch()

topics = get_topics()
rake = Rake()
index = 'news_track'


def use_Rake():
    answer_file = 'answer_rake.txt'
# get topics as a dic
    for num,search_id in topics.items():
        # build query dsl
        dsl = {
            'query': {
                'match': {
                }
            },
            'size': 200
        }
        answer = {}
        # source article
        article = es.get(index=index,id=search_id)['_source']
        title = article['title']
        contents = article['contents']

        # keyword extraction using Rake
        key_words = rake.run(contents)
        # get top-10 keywords
        if len(key_words)>10:
            key_words = key_words[:10]
        # keywords search
        for key_word in key_words:
            match = dsl['query']['match']
            match['contents'] = key_word[0]
            # keyword weight
            confidence = key_word[1]
            key_word_search = es.search(index=index, body=dsl, _source=False)
            hits = key_word_search['hits']
            max_score = hits['max_score']
            hits = hits['hits']
            for hit in hits:
                id = hit['_id']
                score = hit['_score']/max_score
                # score normalization and weighted
                answer[id] = answer.get(id,0) + score * confidence

        # title search
        dsl['query']['match'] = {'title':title}
        title_search = es.search(index=index, body=dsl, _source=False)
        hits = title_search['hits']
        max_score = hits['max_score']
        hits = hits['hits']
        for hit in hits:
            id = hit['_id']
            # title score normalization
            score = hit['_score'] / max_score
            answer[id] = answer.get(id, 0) + score
        answers = sorted(answer.items(), key=lambda d: d[1], reverse=True)
        with open(answer_file,'a') as af:
            written = 0
            for line in answers:
                af.write('{}\tQ0\t{}\t1\t{}\tzzp\n'.format(num,line[0],line[1]))
                written +=1
                if written == 100:
                    break
def use_more_like_this():
    answer_file = 'answer_more.txt'

    news_ea = {
        "query": {
            "more_like_this": {
                "fields": ["title", "contents"],
                "like": [
                    {
                        # "_id": "9171debc316e5e2782e0d2404ca7d09d"
                    }
                ],
                "min_term_freq": 1,
                "max_query_terms": 200
            }
        },
        "size":200
    }
    for num,search_id in topics.items():
        answer = {}
        like = news_ea['query']['more_like_this']['like'][0]
        like['_id'] = search_id
        search_res = es.search(index=index,body=news_ea,_source=False)
        print(search_res)
        hits = search_res['hits']
        max_score = hits['max_score']
        hits = hits['hits']
        for hit in hits:
            id = hit['_id']
            # title score normalization
            score = hit['_score'] / max_score
            answer[id] = answer.get(id, 0) + score
        answers = sorted(answer.items(), key=lambda d: d[1], reverse=True)
        with open(answer_file, 'a') as af:
            written = 0
            for line in answers:
                af.write('{}\tQ0\t{}\t1\t{}\tzzp\n'.format(num, line[0], line[1]))
                written += 1
                if written == 200:
                    break
use_more_like_this()
use_Rake()