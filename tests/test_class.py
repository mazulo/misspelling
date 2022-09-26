#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import unittest

import misspellings_lib as misspellings


BASE_PATH = os.path.dirname(__file__)


class Tests(unittest.TestCase):
    def test_missing_ms_list(self):
        with self.assertRaises(IOError):
            misspellings.Misspellings(
                os.path.join(BASE_PATH, 'missing_msl.txt')
            )

    def test_broken_ms_list(self):
        with self.assertRaises(ValueError):
            misspellings.Misspellings(
                os.path.join(BASE_PATH, 'broken_msl.txt')
            )

    def test_missing_file(self):
        ms = misspellings.Misspellings()
        errors, results = ms.check(os.path.join(BASE_PATH, 'missing_source.c'))
        self.assertTrue(errors)

    def test_good_file(self):
        ms = misspellings.Misspellings()
        errors, results = ms.check(
            os.path.join(BASE_PATH, 'nine_mispellings.c')
        )
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(results), 9)

    def test_more_complex_file(self):
        ms = misspellings.Misspellings()
        errors, results = ms.check(
            os.path.join(BASE_PATH, 'various_spellings.c')
        )
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(results), 7)


class UtilityFunctionTestCase(unittest.TestCase):
    def test_same_case(self):
        self.assertEqual(
            'Apple',
            misspellings.same_case(source='Apple', destination='apple'),
        )

        # Do not make lowercase as "Apple" may be the first word in a sentence.
        self.assertEqual(
            'Apple',
            misspellings.same_case(source='apple', destination='Apple'),
        )

    def test_same_case_with_empty_destination(self):
        self.assertEqual(
            '', misspellings.same_case(source='apple', destination='')
        )
        self.assertEqual(
            '', misspellings.same_case(source='Apple', destination='')
        )

    def test_same_case_with_empty_source(self):
        self.assertEqual(
            'apple', misspellings.same_case(source='', destination='apple')
        )
        self.assertEqual(
            'Apple', misspellings.same_case(source='', destination='Apple')
        )

    def test_split_words(self):
        self.assertEqual(
            ['one', 'two', 'three'], misspellings.split_words('one two three')
        )

    def test_split_words_with_underscores(self):
        self.assertEqual(
            ['one', 'two', 'three'], misspellings.split_words('one_two_three')
        )
        self.assertEqual(
            ['one', 'two', 'three'],
            misspellings.split_words('one__two__three'),
        )
        self.assertEqual(
            ['one', 'two', 'three', 'four'],
            misspellings.split_words('one_two_three four'),
        )

    def test_split_words_with_punctuation(self):
        self.assertEqual(['one', 'two'], misspellings.split_words('one, two'))
        self.assertEqual(
            ['a', 'sentence', ''], misspellings.split_words('a sentence.')
        )

    def test_split_words_with_numbers(self):
        self.assertEqual(
            ['upper', 'lower'], misspellings.split_words('upper2lower')
        )

    def test_split_words_with_camel_case(self):
        self.assertEqual(
            ['one', 'Two', 'Three'], misspellings.split_words('oneTwoThree')
        )
        self.assertEqual(
            ['one', 'Two', 'Three', 'Four'],
            misspellings.split_words('oneTwoThreeFour'),
        )
        self.assertEqual(
            ['one', 'Two', 'Three', 'four'],
            misspellings.split_words('oneTwoThree_four'),
        )
        self.assertEqual(
            ['one', 'Two', 'Three', 'four', 'five'],
            misspellings.split_words('oneTwoThree_four five'),
        )
        self.assertEqual(
            ['foo', 'Up', 'To', 'Bar'], misspellings.split_words('fooUpToBar')
        )

    def test_split_words_with_other_characters(self):
        self.assertEqual(
            ['the', 'big', 'cat'], misspellings.split_words('the%big$cat')
        )

    def test_normalize(self):
        self.assertEqual('alpha', misspellings.normalize('"alpha".'))


if __name__ == '__main__':
    unittest.main()
