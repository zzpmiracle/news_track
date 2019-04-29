import pysolr
# Create a client instance. The timeout and authentication options are not required.
solr = pysolr.Solr('http://localhost:8983/solr/', always_commit=True)

solr.add([
    {
        "id": "doc_1",
        "title": "A test document",
    },
    {
        "id": "doc_2",
        "title": "The Banana: Tasty or Dangerous?",
        "_doc": [
            { "id": "child_doc_1", "title": "peel" },
            { "id": "child_doc_2", "title": "seed" },
        ]
    },
])
results = solr.search('bananas')
print("Saw {0} result(s).".format(len(results)))

# Just loop over it to access the results.
for result in results:
    print("The title is '{0}'.".format(result['title']))

# For a more advanced query, say involving highlighting, you can pass
# additional options to Solr.
results = solr.search('bananas', **{
    'hl': 'true',
    'hl.fragsize': 10,
})

# You can also perform More Like This searches, if your Solr is configured
# correctly.
similar = solr.more_like_this(q='id:doc_2', mltfl='text')

# Finally, you can delete either individual documents,
solr.delete(id='doc_1')

# also in batches...
solr.delete(id=['doc_1', 'doc_2'])

# ...or all documents.
solr.delete(q='*:*')