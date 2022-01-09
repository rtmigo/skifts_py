# [skifts](https://github.com/rtmigo/skifts_py#readme)

Searches for the most relevant documents containing words from a query.

For example:

```python3
query = ['A', 'B']

documents = [
    ['N', 'A', 'M'],  # common features: 'A'
    ['C', 'B', 'A'],  # common features: 'A', 'B'  
    ['X', 'Y']  # no common features
]
```

In this case, the search with return `['C', 'B', 'A']` and `['N', 'A',
'M']` in that particular order.

## Install

```bash
pip3 install git+https://github.com/rtmigo/skifts_py#egg=skifts
```

## Use for full-text search

Finding documents that contain words from the query.

```python3
from skifts import SkiFts

# three documents, one per row
documents = [
    ["wait", "mister", "postman"],
    ["please", "mister", "postman", "look", "and", "see"],
    ["oh", "yes", "wait", "a", "minute", "mister", "postman"]
] 

fts = SkiFts(documents)

# find and print the most relevant documents:
for doc_index in fts.search(['postman', 'wait']):
    print(documents[doc_index])
```

## Implementation details

The search uses the [scikit-learn](https://scikit-learn.org) library, which 
ranks documents using [tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) and
[cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity).
