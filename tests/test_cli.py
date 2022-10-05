#!/usr/bin/env python

import os
import subprocess
import unittest


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
CLI = os.path.join(BASE_PATH, os.pardir, 'misspellings')


class TestCli:

    """Test the CLI.

    USAGE: misspellings [-f file] [files]
    Checks files for common spelling mistakes.
      -f file: File containing list of files to check.
      -m file: File containing list of misspelled words & corrections.
      -d     : Dump the list of misspelled words.
      -s file: Create a shell script to interactively correct the file.
      files: Zero or more files to check.

    """

    def test_good_file(self):
        p = subprocess.Popen(
            [CLI, 'nine_mispellings.c'],
            cwd=BASE_PATH,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert error_output.decode() ==  ''
        assert len(output.decode().split('\n')) ==  10
        assert p.returncode ==  2

    def test_bad_file(self):
        p = subprocess.Popen(
            [CLI, 'missing.c'],
            cwd=BASE_PATH,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert output.decode() == ''
        assert len(error_output.decode().split('\n')) == 2
        assert p.returncode == 0

    def test_good_flag_f(self):
        p = subprocess.Popen(
            [CLI, '-f', 'good_file_list'],
            cwd=BASE_PATH,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert error_output.decode() == ''
        assert len(output.decode().split('\n')) == 10
        assert p.returncode == 2

    def test_bad_flag_f(self):
        p = subprocess.Popen(
            [CLI, '-f', 'broken_file_list'],
            cwd=BASE_PATH,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert output.decode() == ''
        assert len(error_output.decode().split('\n')) == 2
        assert p.returncode == 0


    def test_bad_flag_m(self):
        p = subprocess.Popen(
            [CLI, '-d', '-m', 'broken_msl.txt'],
            cwd=BASE_PATH,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert 'ValueError' in error_output.decode()
        assert output.decode() == ''
        assert p.returncode == 1

    def test_good_flag_m(self):
        p = subprocess.Popen(
            [CLI, '-d', '-m', 'small_msl.txt'],
            cwd=BASE_PATH,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert error_output.decode() == ''
        assert len(output.decode().split('\n')) == 3
        assert p.returncode == 0

    def test_passing_misspelling_json_file(self):
        p = subprocess.Popen(
            [CLI, '-d', '-j', 'nine_mispellings.json'],
            cwd=BASE_PATH,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert error_output.decode() == ''
        assert len(output.decode().split('\n')) == 10
        assert p.returncode == 0

    def test_bad_flag_s(self):
        p = subprocess.Popen(
            [CLI, '-s', 'various_spellings.c'],
            cwd=BASE_PATH,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert 'must not exist' in error_output.decode()
        assert output.decode() == ''
        assert p.returncode == 2

    def test_good_flag_s(self):
        test_out = os.path.join(BASE_PATH, 'various_spellings.test_out')
        good_out = os.path.join(BASE_PATH, 'various_spellings.good_out')
        if os.path.exists(test_out):
            os.unlink(test_out)
        p = subprocess.Popen(
            [CLI, '-s', test_out, 'various_spellings.c'],
            cwd=BASE_PATH,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        (output, error_output) = p.communicate(input='\n'.encode('utf8'))
        assert error_output.decode() == ''
        assert 'withdrawl' in output.decode()
        assert p.returncode == 0

        with open(good_out, 'r') as good_file:
            good_contents = good_file.readlines()
        with open(test_out, 'r') as test_file:
            test_contents = test_file.readlines()
        assert test_contents == good_contents

    def test_standard_in(self):
        p = subprocess.Popen(
            [CLI, '-f', '-'],
            cwd=BASE_PATH,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        (output, error_output) = p.communicate(
            input='nine_mispellings.c\n'.encode('utf8')
        )
        assert error_output.decode() == ''
        assert len(output.decode().split('\n')) == 10
        assert p.returncode == 2