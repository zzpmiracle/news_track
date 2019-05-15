[TOC]

## DataSet

### Initial structure

* 595,037 documents
* **article**  :  id |  url  |  title  |  kicker  | author  |  published_date  |  contents  |  type  |  sourse
  * contents
    * (None)
    * kicker : a section header indicating the publication category，**irrelevant** if is one of  "Opinion", "Letters to the Editor","The Post's View"
    * title 
    * image : image URL and full caption
    * byline : by + author(s)
    * **paragraph** :  plain (text)  |  html (with html style < …… >)
    * (author_info)
  * type  : 'article' / 'blog'
  * sourse : 'The Washington Post'

### Data cleaning
  * remove irrelevant article according to kicker
  * remove ['type'] ,['sourse'] rom article
  * remove [byline] ,[title] ,[author_info] ,[image] from contents if exist
  * remove empty content from contents
  * remove html code from content 
  * group contents into an article (plain text)

### After cleaning

* 571,963 docs remained
* **article**  :  id  |  url  |  title  |  kicker  | author  |  date  |  contents(long string)

## ElasticSearch
### Steps
1. insert：id + other parts
2. topics  :  BeautifulSoup --> id + num
3. source article : id in ES
4. search : title and 10 keywords(Rake) respectively
5. sort : score normalization --> weighted(from Rake) sum

### Result

nearly irrelevant

### Next plans

* other keyword extraction algorithm
* divide into 5 relevance level
* other algorithm to judge relevance