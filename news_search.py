from elasticsearch import Elasticsearch


from pyhanlp import HanLP
dst_file_path = 'D:\TREC_v2.txt'
with open(dst_file_path) as f:
    line = next(f)

    print(HanLP.extractKeyword(line, 200))
