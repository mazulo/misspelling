import os
import subprocess
from pathlib import Path

TEST_BASE_DIR = Path(__file__).parents[0]
CLI = Path(__file__).parents[1] / "src/misspelling_lib/misspellings.py"


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
            [CLI, "test_assets/nine_misspellings.c"],
            cwd=TEST_BASE_DIR,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert error_output.decode() == ""
        assert len(output.decode().split("\n")) == 10
        assert p.returncode == 2

    def test_good_file_with_ignore_misspelling_comment(self):
        p = subprocess.Popen(
            [CLI, "test_assets/nine_misspellings_with_ignore.c"],
            cwd=TEST_BASE_DIR,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert error_output.decode() == ""
        assert len(output.decode().split("\n")) == 9
        assert p.returncode == 2

    def test_bad_file(self):
        p = subprocess.Popen(
            [CLI, "test_assets/missing.c"],
            cwd=TEST_BASE_DIR,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert output.decode() == ""
        assert len(error_output.decode().split("\n")) == 2
        assert p.returncode == 0

    def test_good_flag_f(self):
        p = subprocess.Popen(
            [CLI, "--file-list", "test_assets/good_file_list"],
            cwd=TEST_BASE_DIR,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert error_output.decode() == ""
        assert len(output.decode().split("\n")) == 10
        assert p.returncode == 2

    def test_bad_flag_f(self):
        p = subprocess.Popen(
            [CLI, "--file-list", "test_assets/broken_file_list"],
            cwd=TEST_BASE_DIR,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert output.decode() == ""
        assert len(error_output.decode().split("\n")) == 2
        assert p.returncode == 0

    def test_bad_flag_m(self):
        p = subprocess.Popen(
            [
                CLI,
                "--dump-misspelling",
                "--misspelling-file",
                "test_assets/broken_msl.txt",
            ],
            cwd=TEST_BASE_DIR,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert "ValueError" in error_output.decode()
        assert output.decode() == ""
        assert p.returncode == 1

    def test_good_flag_m(self):
        p = subprocess.Popen(
            [
                CLI,
                "--dump-misspelling",
                "--misspelling-file",
                "test_assets/small_msl.txt",
            ],
            cwd=TEST_BASE_DIR,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert error_output.decode() == ""
        assert len(output.decode().split("\n")) == 3
        assert p.returncode == 0

    def test_passing_misspelling_json_file(self):
        p = subprocess.Popen(
            [
                CLI,
                "--dump-misspelling",
                "--json-file",
                "test_assets/nine_misspellings.json",
            ],
            cwd=TEST_BASE_DIR,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert error_output.decode() == ""
        assert len(output.decode().split("\n")) == 10
        assert p.returncode == 0

    def test_bad_flag_s(self):
        p = subprocess.Popen(
            [CLI, "--script-output", "test_assets/various_spellings.c"],
            cwd=TEST_BASE_DIR,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        (output, error_output) = p.communicate()
        assert "must not exist" in error_output.decode()
        assert output.decode() == ""
        assert p.returncode == 2

    def test_good_flag_s(self):
        test_out = TEST_BASE_DIR.joinpath("test_assets/various_spellings.test_out")
        good_out = TEST_BASE_DIR.joinpath("test_assets/various_spellings.good_out")
        if os.path.exists(test_out):
            os.unlink(test_out)
        p = subprocess.Popen(
            [
                CLI,
                "--script-output",
                "test_assets/various_spellings.test_out",
                "test_assets/various_spellings.c",
            ],
            cwd=TEST_BASE_DIR,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        (output, error_output) = p.communicate(input="\n".encode("utf8"))
        assert error_output.decode() == ""
        assert "withdrawl" in output.decode()  # ignore-misspelling
        assert p.returncode == 0

        with open(good_out, "r", encoding="utf-8") as good_file:
            good_contents = good_file.readlines()
        with open(test_out, "r", encoding="utf-8") as test_file:
            test_contents = test_file.readlines()
        assert test_contents == good_contents

    def test_standard_in(self):
        p = subprocess.Popen(
            [CLI, "--file-list", "-"],
            cwd=TEST_BASE_DIR,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        (output, error_output) = p.communicate(input="test_assets/nine_misspellings.c\n".encode("utf8"))
        assert error_output.decode() == ""
        assert len(output.decode().split("\n")) == 10
        assert p.returncode == 2
