# misspelling

## Spell checker for code

> This is a project originally forked from https://github.com/erichurkman/misspellings

This is a Python library and tool to check for misspelled words in
source code. It does this by looking for words from a list of
common misspellings. The dictionary it uses to do this is based
on the Wikipedia list of common misspellings.

- http://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines

The list has been slightly modified to remove some changes that
cause a number of false positives. In particular `ok->OK` was
removed (ok is frequently used in perl tests for instance).


## Opinionated version

This includes custom additions that should be considered opinionated, such as
cancellation vs. cancelation. This is not recommended for anyone's use.


## Contributions

Contributions are welcome! Please add unit tests for new features
or bug fixes. To run all the unit tests run `pytest tests/`.

You can review `coverage` of added tests by running `pytest --cov=tests`.

Note that tests are run on `GitHub Actions` for all supported python versions whenever the tree on GitHub is pushed to.

The packaged version is available via `pip` or `easy_install` as `misspellings-lib`. The project page is on `pypi`:

The source code is available in the following locations:

- Bitbucket: https://bitbucket.org/lyda/misspell-check/src
- code.google: http://code.google.com/p/misspell-check/
- Github: https://github.com/lyda/misspell-check
- Gitorious: https://gitorious.org/uu/misspell-check
- Sourceforge: https://sourceforge.net/p/misspell-check
- Mazulo's GitHub: https://github.com/mazulo/misspelling

Pull requests on any of those platforms or emailed patches are fine.

## To do

Some items on the TODO list:

- Implement option to interactively fix files.
- Give some thought to supporting multiple languages?
- Might a "common misspellings" list be different for different English
  users - might an American make one set of mistakes while a German
  writing English make another? Source of this data?
- Fix sed flag. We need to have it support sed -i optionally, have it output all
  unambiguous sed commands, have it be more careful on what it
  replaces. It might also be an idea to have a perl output option.
- Use generators to allow finding errors as you go. However, currently misspellings
  grabs all files first, then checks them, which can take a while.
- Lacking tests for misspellings cli.


## Credits

- `Kevin Lyda`: Initial shell goo and python version.
- `Steven Myint`: Better python idioms and style. Mixed case support. Travis/tox support.
- `Maciej Blizinski`: Potential use in `OpenCSW` pushed move to python.
- `Ville Skyttä`: Sped up wordification, editor-friendly reporting.

- `coverage`: https://pypi.python.org/pypi/coverage
- `Kevin Lyda`: https://github.com/lyda
- `Steven Myint`: https://github.com/myint
- `Maciej Blizinski`: https://github.com/automatthias
- `Ville Skyttä`: https://github.com/scop
- `pypi`: https://pypi.python.org/pypi/misspellings
- `OpenCSW`: http://www.opencsw.org/
