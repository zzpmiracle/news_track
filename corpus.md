[TOC]

# 数据集

595,037 documents

## 初始

* article

  * id : document identification
  * article_url : URL of the publication
  * title : document main title
  * author : author(s) of the publication
  *  published_date : publication date in timestamp format.
  * contents
    * (None)
    * kicker : a section header indicating the publication category
    * title
    * image
    * byline : by + author(s)
    * paragraph 
      * plain (text)
      * html (with html style < …… >)
    * (author_info)
  * type  : 'article' / 'blog'
  * sourse : 'The Washington Post'

## Data cleaning
  * remove ['type'] ,['sourse'] rom article
  * move contents['full caption'] to article
  * remove [byline] ,[title] ,[author_info] ,[image] from contents if exist
  * remove html code from content with 
  * change contents to list of paragraph (plain text)
  * remove None from contents

## after cleaning

* article

  - id
  - url
  - title
  - kicker
  - author
  - date
  - contents: [ plain text  * n ]
