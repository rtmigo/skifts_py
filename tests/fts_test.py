# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

import re
import unittest

from typing import List

from npfts._npfts import SkFts

_mr_postman = """
    "Please Mr. Postman" is a song written 
    by Georgia Dobbins, William Garrett,
    Freddie Gorman, Brian Holland and Robert Bateman

    Oh yes, wait a minute Mister Postman
    (Wait)
    Wait Mister Postman
    Please Mister Postman, look and see
    (Oh yeah)
    If there's a letter in your bag for me
    (Please, Please Mister Postman)
    Why's it takin' such a long time
    (Oh yeah)
    For me to hear from that boy of mine
    There must be some word today
    From my boyfriend so far away
    Please Mister Postman, look and see
    If there's a letter, a letter for me
    I've been standin' here waitin' Mister Postman
    So patiently
    For just a card, or just a letter
    Sayin' he's returnin' home to me
    Mister Postman, look and see
    (Oh yeah)
    If there's a letter in your bag for me
    (Please, Please Mister Postman)
    Why's it takin' such a long time
    (Oh yeah)
    For me to hear from that boy of mine
    So many days you passed me by
    See the tears standin' in my eyes
    You didn't stop to make me feel better
    By leavin' me a card or a letter
    Mister Postman, look and see
    If there's a letter in your bag for me
    (Please, Please Mister Postman)
    Why's it takin' such a long time
    Wait a minute
    Wait a minute
    Wait a minute
    Wait a minute
    (Mister Postman)
    Mister Postman, look and see
"""


def _words(text: str) -> List[str]:
    return [w.lower() for w in re.findall(r'\w+', text)]

def _postman_corpus():
    return [_words(line) for line in _mr_postman.splitlines()]

class TestFts(unittest.TestCase):

    def createFts(self, corpus):
        return SkFts(corpus)

    def test(self):
        corpus = _postman_corpus()

        db = self.createFts(corpus)


        def idx_to_doc(idx):
            return corpus[idx]

        def best_match(query):
            return idx_to_doc(db.search(query)[0])

        self.assertEqual(
            best_match(['yeah']),
            ['oh', 'yeah'])

        self.assertEqual(
            best_match(['wait']),
            ['wait'])

        self.assertEqual(
            best_match(['minute']),
            ['wait', 'a', 'minute'])

        self.assertEqual(
            best_match(['please', 'postman']),
            ['please', 'please', 'mister', 'postman'])

        self.assertEqual(
            best_match(['wait', 'postman']),
            ['wait', 'mister', 'postman'])

        self.assertEqual(
             len(db.search(['jabberwocky'])), 0)

    @unittest.skip
    def test_empty_query(self):
        db = self.createFts()
        for doc in [
            [2, 3],
            [1, 2, 3],
            [1, 3, 4, 2]
        ]:
            db.add(doc_id=str(doc), words=doc)

        db.search([1])  # no problem
        with self.assertRaises(ValueError):
            db.search([])

    @unittest.skip
    def test_nums(self):

        db = self.createFts()
        for doc in [
            [2, 3],
            [1, 2, 3],
            [1, 3, 4, 2]
        ]:
            db.add(doc_id=str(doc), words=doc)

        # при поиске единицы найдем самую короткую последовательность
        # с ней
        r = db.search([1])
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], '[1, 2, 3]', )

        # числа [2, 3] есть в каждой из последовательностей.
        # Короткие будут первыми
        q = [2, 3]
        r = db.search(q)
        self.assertEqual(len(r), 3)
        self.assertEqual(r[0], '[2, 3]')
        self.assertEqual(r[1], '[1, 2, 3]')

        # число 4 в сочетании с 1 есть только в одной последовательности.
        # Она будет первой
        q = [4, 1]
        r = db.search(q)
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], '[1, 3, 4, 2]')
        self.assertEqual(r[1], '[1, 2, 3]')

    @unittest.skip
    def test_number_of_matched_words(self):

        db = self.createFts()
        for doc in [
            [1, 2, 3],
            [3, 2, 1],
            [2, 3, 5],  # !
            [2, 3, 1],
            [1, 3, 2],

        ]:
            db.add(doc_id=str(doc), words=doc)

        q = [1, 2, 3, 5]

        r = db.search(q)
        # всего два совпадения, но приоритетное слово
        self.assertEqual(r[0], '[2, 3, 5]')

    @unittest.skip
    def test_word_popularity(self):

        db = self.createFts()
        for doc in [
            [1, 2],
            [1, 3],
            [7, 5],
            [1, 4],
            [9, 8]
        ]:
            db.add(doc_id=str(doc), words=doc)

        # не будет ни одного полного совпадения, но первым найдется
        # совпадение с редкой пятеркой

        q = [1, 5]
        r = db.search(q)
        self.assertEqual(len(r), 4)
        self.assertEqual(r[0], '[7, 5]')

    @unittest.skip
    def test_not_unique_id(self):
        fts = self.createFts()
        fts.add(['a', 'b', 'c'], doc_id='id1')
        with self.assertRaises(ValueError):
            fts.add(['d', 'e', 'f'], doc_id='id1')

    @unittest.skip
    def test_not_passing_id(self):
        fts = self.createFts()
        ids = set()
        ids.add(fts.add(['a', 'b', 'c']))
        ids.add(fts.add(['d', 'e']))
        ids.add(fts.add(['f', 'g']))
        self.assertEqual(len(ids), 3)
