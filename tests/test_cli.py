import os
from pathlib import Path
import subprocess


TEST_BASE_DIR = Path(__file__).parents[0]
BASE_PATH = Path(__file__).parents[1]
CLI = Path(__file__).parents[1].joinpath('misspellings').as_posix()


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
        nine_misspellings = TEST_BASE_DIR.joinpath('tests/assets/nine_misspellings.c').as_posix()
        p = subprocess.Popen(
            [CLI, 'assets/nine_misspellings.c'],
            cwd=TEST_BASE_DIR.as_posix(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert error_output.decode() == ''
        assert len(output.decode().split('\n')) == 10
        assert p.returncode == 2

    def test_bad_file(self):
        missing = TEST_BASE_DIR.joinpath('assets/missing.c').as_posix()
        p = subprocess.Popen(
            [CLI, missing],
            cwd=BASE_PATH.as_posix(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert output.decode() == ''
        assert len(error_output.decode().split('\n')) == 2
        assert p.returncode == 0

    def test_good_flag_f(self):
        good_file_list = TEST_BASE_DIR.joinpath('assets/good_file_list').as_posix()
        p = subprocess.Popen(
            [CLI, '--file_list', good_file_list],
            cwd=BASE_PATH.as_posix(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert error_output.decode() == ''
        assert len(output.decode().split('\n')) == 10
        assert p.returncode == 2

    def test_bad_flag_f(self):
        broken_file_list = TEST_BASE_DIR.joinpath('assets/broken_file_list').as_posix()
        p = subprocess.Popen(
            [CLI, '--file_list', broken_file_list],
            cwd=BASE_PATH.as_posix(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert output.decode() == ''
        assert len(error_output.decode().split('\n')) == 2
        assert p.returncode == 0

    def test_bad_flag_m(self):
        broken_msl = TEST_BASE_DIR.joinpath('assets/broken_msl.txt').as_posix()
        p = subprocess.Popen(
            [CLI, '--dump_misspelling', '--misspelling_file', broken_msl],
            cwd=BASE_PATH.as_posix(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert 'ValueError' in error_output.decode()
        assert output.decode() == ''
        assert p.returncode == 1

    def test_good_flag_m(self):
        small_msl = TEST_BASE_DIR.joinpath('assets/small_msl.txt').as_posix()
        p = subprocess.Popen(
            [CLI, '--dump_misspelling', '--misspelling_file', small_msl],
            cwd=BASE_PATH.as_posix(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert error_output.decode() == ''
        assert len(output.decode().split('\n')) == 3
        assert p.returncode == 0

    def test_passing_misspelling_json_file(self):
        nine_misspellings = TEST_BASE_DIR.joinpath('assets/nine_misspellings.json').as_posix()
        p = subprocess.Popen(
            [CLI, '--dump_misspelling', '--json_file', nine_misspellings],
            cwd=BASE_PATH.as_posix(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert error_output.decode() == ''
        assert len(output.decode().split('\n')) == 10
        assert p.returncode == 0

    def test_bad_flag_s(self):
        various_spellings = TEST_BASE_DIR.joinpath('assets/various_spellings.c').as_posix()
        p = subprocess.Popen(
            [CLI, '--script_output', various_spellings],
            cwd=BASE_PATH.as_posix(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert 'must not exist' in error_output.decode()
        assert output.decode() == ''
        assert p.returncode == 2

    def test_good_flag_s(self):
        test_out = TEST_BASE_DIR.joinpath('assets/various_spellings.test_out').as_posix()
        good_out = TEST_BASE_DIR.joinpath('assets/various_spellings.good_out').as_posix()
        various_spellings = TEST_BASE_DIR.joinpath('assets/various_spellings.c').as_posix()
        if os.path.exists(test_out):
            os.unlink(test_out)
        p = subprocess.Popen(
            [CLI, '--script_output', 'tests/assets/various_spellings.test_out', 'tests/assets/various_spellings.c'],
            cwd=BASE_PATH.as_posix(),
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
        nine_misspellings = TEST_BASE_DIR.joinpath('assets/nine_misspellings.c').as_posix()
        p = subprocess.Popen(
            [CLI, '--file_list', '-'],
            cwd=BASE_PATH.as_posix(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        (output, error_output) = p.communicate(
            input=f'tests/assets/nine_misspellings.c\n'.encode('utf8')
        )
        assert error_output.decode() == ''
        assert len(output.decode().split('\n')) == 10
        assert p.returncode == 2
