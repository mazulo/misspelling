#!/usr/bin/env python3

import json
import sys
from collections import OrderedDict


def convert_into_json():
    word_dict = {}
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print('No file provided.')
        sys.exit(0)

    with open(filename) as wikipedia_file:
        for line in wikipedia_file.readlines():
            wrong_word, right_words = line.split('->')
            list_right_words = []
            if ',' in right_words:
                list_right_words = [word for word in right_words.split(',')]
            corrections = []
            if list_right_words:
                for word in list_right_words:
                    # print(f"word inside loop: {word}")
                    word: str = (
                        word.replace('"', '')
                        .replace('\\', '')
                        .replace('\n', '')
                        .replace(' ', '')
                    )
                    corrections.extend([word])
            elif '\n' in right_words:
                right_words: str = right_words.replace('\n', '')
                corrections.extend([right_words])
            word_dict[wrong_word] = corrections

    with open(filename, 'w') as wikipedia_file:
        ordered_dict = OrderedDict(
            sorted(word_dict.items(), key=lambda t: t[0])
        )
        json.dump(ordered_dict, wikipedia_file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    convert_into_json()
