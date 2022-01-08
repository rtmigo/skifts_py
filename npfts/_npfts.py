from typing import NamedTuple, List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# corpus = [
#     'This is the first document.',
#     'This document is the second document.',
#     'And this is the third one.',
#     'Is this the first document?',
# ]


# print(X)
# print(vectorizer.get_feature_names_out())
# >>> print(X.shape)

def _pass(arg):
    return arg


class Found(NamedTuple):
    doc_idx: int
    score: float


class Finder:
    # https://stackoverflow.com/a/55682395
    def __init__(self, corpus):
        self._docs_count = len(corpus)
        self._vectorizer = TfidfVectorizer(tokenizer=_pass, preprocessor=_pass)
        self._tfidf = self._vectorizer.fit_transform(corpus)

    # def _tokenize(self, text: List[str]) -> List[str]:
    #     return text

    def search(self, query):
        query_tfidf = self._vectorizer.transform(query)
        sim = cosine_similarity(query_tfidf, self._tfidf).flatten()
        assert self._docs_count == sim.shape[0]
        n = sim.shape[0]
        new_row = np.arange(0, n, 1)
        # print(new_row)
        # print(sim)
        # print("="*80)

        matrix = np.vstack([sim, new_row])
        # print("MATRIX")
        # print(matrix)
        # print("-" * 80)
        # сортируем по значению первой строки (по возрастанию)
        matrix = matrix[:, matrix[0, :].argsort()]

        # (переворачиваем, чтобы это была сортировка по убыванию)
        matrix = matrix[:, ::-1]

        result: List[int] = []
        for score, doc_idx in matrix.transpose():
            if score <= 0:
                assert score == 0
                break
            result.append(int(doc_idx))

        return result
        # print(score, int(doc_idx))
        # matrix = np.swapaxes(matrix)
        # A = np.fliplr(A)
        # A.sort(axis=1)
        # print(matrix)

# f = Finder(corpus)
# f.search('third')
