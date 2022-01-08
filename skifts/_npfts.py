# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SkFts:
    # https://stackoverflow.com/a/55682395
    def __init__(self, corpus: List[List[str]]):
        self._docs_count = len(corpus)

        self._vectorizer = TfidfVectorizer(
            # Я не хочу, чтобы SciPy делила текст на токены: я буду сразу
            # подавать на вход списки. Поэтому задаю следующие аргументы как
            # ничего не делающие
            tokenizer=lambda x: x,
            preprocessor=lambda x: x)
        self._docs_tfidf = self._vectorizer.fit_transform(corpus)

    def search(self, query: List[str]) -> List[int]:
        query_tfidf = self._vectorizer.transform([query])
        scores = cosine_similarity(query_tfidf, self._docs_tfidf).flatten()
        assert self._docs_count == scores.shape[0]

        # Сейчас scores - это одномерный массив, в котором каждый элемент
        # соответствует документу и равен релевантности этого документа.
        # Превратим массив в двумерный: второй строкой будут индексы
        # документов
        n = scores.shape[0]
        indexes = np.arange(0, n, 1)
        assert indexes.shape[0] == scores.shape[0]
        matrix = np.vstack([scores, indexes])

        # Сортируем двумерный массив по значению первой строки. При этом
        # меняются обе строки: в первой будет возрастающий список
        # релевантностей, а во второй переупорядоченные индексы документов
        matrix = matrix[:, matrix[0, :].argsort()]

        # Переворачиваем массив наоборот, чтобы значения релевантности шли
        # от больших к меньшим, а нули (нерелевантные документы) в конце
        matrix = matrix[:, ::-1]

        result: List[int] = []
        for score, doc_idx in matrix.transpose():
            if score <= 0:
                # значения score убывают - дальше будут только нули
                assert score == 0
                break
            result.append(int(doc_idx))

        # может лучше было удалить нули на уровне numpy? Не уверен

        return result
