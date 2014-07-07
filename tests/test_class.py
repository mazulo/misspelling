#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import unittest

import misspellings_lib as misspellings


BASE_PATH = os.path.dirname(__file__)
LOG_PATH = os.path.join(BASE_PATH, 'logs')


class MisspellingsTestCase(unittest.TestCase):

    def setUp(self):
        try:
            os.mkdir(LOG_PATH)
        except:
            pass

    def testMissingMSList(self):
        with self.assertRaises(IOError):
            misspellings.Misspellings(
                os.path.join(BASE_PATH, 'missing_msl.txt'))

    def testBrokenMSList(self):
        with self.assertRaises(ValueError):
            misspellings.Misspellings(
                os.path.join(BASE_PATH, 'broken_msl.txt'))

    def testMissingFile(self):
        ms = misspellings.Misspellings()
        errors, results = ms.check(os.path.join(BASE_PATH, 'missing_source.c'))
        self.assertTrue(errors)

    def testGoodFile(self):
        ms = misspellings.Misspellings()
        errors, results = ms.check(
            os.path.join(BASE_PATH, 'nine_mispellings.c'))
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(results), 9)

    def testMoreComplexFile(self):
        ms = misspellings.Misspellings()
        errors, results = ms.check(
            os.path.join(BASE_PATH, 'various_spellings.c'))
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(results), 7)


class UtilityFunctionTestCase(unittest.TestCase):

    def testSameCase(self):
        self.assertEqual('Apple', misspellings.same_case(source='Apple',
                                                         destination='apple'))

        # Do not make lowercase as "Apple" may be the first word in a sentence.
        self.assertEqual('Apple', misspellings.same_case(source='apple',
                                                         destination='Apple'))

    def testSameCaseWithEmptyDestination(self):
        self.assertEqual('', misspellings.same_case(source='apple',
                                                    destination=''))
        self.assertEqual('', misspellings.same_case(source='Apple',
                                                    destination=''))

    def testSameCaseWithEmptySource(self):
        self.assertEqual('apple', misspellings.same_case(source='',
                                                         destination='apple'))
        self.assertEqual('Apple', misspellings.same_case(source='',
                                                         destination='Apple'))

    def testSplitWords(self):
        self.assertEqual(['one', 'two', 'three'],
                         misspellings.split_words('one two three'))

    def testSplitWordsWithUnderscores(self):
        self.assertEqual(['one', 'two', 'three'],
                         misspellings.split_words('one_two_three'))
        self.assertEqual(['one', 'two', 'three'],
                         misspellings.split_words('one__two__three'))
        self.assertEqual(['one', 'two', 'three', 'four'],
                         misspellings.split_words('one_two_three four'))

    def testSplitWordsWithPunctuation(self):
        self.assertEqual(['one', 'two'],
                         misspellings.split_words('one, two'))
        self.assertEqual(['a', 'sentence', ''],
                         misspellings.split_words('a sentence.'))

    def testSplitWordsWithNumbers(self):
        self.assertEqual(['upper', 'lower'],
                         misspellings.split_words('upper2lower'))

    def testSplitWordsWithCamelCase(self):
        self.assertEqual(['one', 'Two', 'Three'],
                         misspellings.split_words('oneTwoThree'))
        self.assertEqual(['one', 'Two', 'Three', 'Four'],
                         misspellings.split_words('oneTwoThreeFour'))
        self.assertEqual(['one', 'Two', 'Three', 'four'],
                         misspellings.split_words('oneTwoThree_four'))
        self.assertEqual(['one', 'Two', 'Three', 'four', 'five'],
                         misspellings.split_words('oneTwoThree_four five'))
        self.assertEqual(['foo', 'Up', 'To', 'Bar'],
                         misspellings.split_words('fooUpToBar'))

    def testSplitWordsWithOtherCharacters(self):
        self.assertEqual(['the', 'big', 'cat'],
                         misspellings.split_words('the%big$cat'))

    def testNormalize(self):
        self.assertEqual('alpha', misspellings.normalize('"alpha".'))


if __name__ == '__main__':
    unittest.main()
