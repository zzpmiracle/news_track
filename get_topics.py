from bs4 import BeautifulSoup
import codecs
import re

def get_topics(filename='D:\\news_track\\newsir18-topics.txt',topic_tag = 'top',num_tag='num',id_tag='docid'):
    soup = BeautifulSoup(codecs.open(filename, "r"), "lxml")
    dic = {}
    for topic in soup.findAll(topic_tag):
        num_str = topic.find(num_tag).getText()
        num = int(re.findall(r'\d+',num_str)[0])
        id = topic.findNext(id_tag).text
        dic[num] = id
    return dic

# print(get_topics())