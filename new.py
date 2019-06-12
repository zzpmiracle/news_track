body ={
"mappings": {
    "properties": {
      "text": {
        "type": "text",
        "term_vector": "with_positions_offsets_payloads",
        "store" : True,
        "analyzer" : "fulltext_analyzer"
       },
       "fullname": {
        "type": "text",
        "term_vector": "with_positions_offsets_payloads",
        "analyzer" : "fulltext_analyzer"
      }
    }
  },
    "settings": {
        "analysis": {
            "fulltext_analyzer": {
                "type": "custom",
                "tokenizer": "whitespace",
                "filter": ["lowercase","type_as_payload"]
            },
            "filter": {
                "en_stop": {
                    "type":       "stop",
                    "stopwords":  "_english_"
                }
            }
        }
    }
}
