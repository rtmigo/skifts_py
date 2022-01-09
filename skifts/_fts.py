# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT
from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skifts._array2d import Array2D


class SkiFts:
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
        """Finds all documents containing at least one word from `query`.
        Returns list of indexes of these documents, starting from most
        relevant."""

        if len(query) <= 0:
            raise ValueError

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
        assert len(indexes.shape) == 1

        matrix = np.vstack([scores, indexes])
        assert len(matrix.shape) == 2
        assert matrix.shape[0] == 2
        assert matrix.shape[1] == n

        # Сортируем двумерный массив по значению первой строки. Элементы
        # обеих строк будут перемещаться. В итоге в первой будет возрастающий
        # список релевантностей, а во второй переупорядоченные индексы
        # документов
        matrix = Array2D.sort_by_first_row(matrix)

        # Переворачиваем массив наоборот, чтобы значения релевантности шли
        # от больших к меньшим, а нули (нерелевантные документы) в конце
        matrix = Array2D.reverse_rows(matrix)

        # Если в первой строке ноль, значит документ не релевантен: не совпало
        # ни одно слово. Удаляем такие колонки из матрицы
        matrix = Array2D.keep_columns_with_nonzero_first_row(matrix)

        # возвращаем вторую строку (в которой индексы документов)
        return matrix[1].astype(int)
