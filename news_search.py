from elasticsearch import Elasticsearch

es = Elasticsearch()

dsl = {
    'query': {
        'match': {
            'title': 'Women in Parliaments'
        }
    }
}
result = es.search(index='news_track',body=dsl,_source=False)
print(result)
import pyhanlp
