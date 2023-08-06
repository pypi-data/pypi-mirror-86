# Setupmeta Builder

![GitHub](https://img.shields.io/github/license/Cologler/setupmeta_builder-python.svg)
[![Build Status](https://travis-ci.com/Cologler/setupmeta_builder-python.svg?branch=master)](https://travis-ci.com/Cologler/setupmeta_builder-python)
[![PyPI](https://img.shields.io/pypi/v/setupmeta_builder.svg)](https://pypi.org/project/setupmeta_builder/)

Try auto build `setup.py` attributes from git commit, CI config, etc.

## Usage

Replace your `setup.py` file to:

```py
from setupmeta_builder import setup_it

setup_it()
```

Done!

`setupmeta_builder` try resolve other values like `install_requires` for you.

| meta fields                    | resolve from                                                 |
| ------------------------------ | ------------------------------------------------------------ |
| `packages`                     | `find_packages()`                                            |
| `name`                         | packages or `pyproject.toml`                                 |
| `version`                      | `git.tag`                                                    |
| `long_description`             | file: `README.rst` or `README.md`                            |
| `author` and `author_email`    | file: `.pkgit.json` or `pyproject.toml`                      |
| `url`                          | `git.origin.url`                                             |
| `license`                      | file: `LICENSE`                                              |
| `classifiers`                  | license and file `.travis.yml`                               |
| `install_requires`             | files: `requirements.txt` or `pipfile` or `pyproject.toml`   |
| `tests_require`                | file: `pipfile` or `pyproject.toml`                          |
| `extras_require`               | files: `requirements.*.txt` or `pyproject.toml`              |
| `entry_points.console_scripts` | `PACKAGE_ROOT\entry_points_console_scripts.py` or `pyproject.toml`. |

Current project is the first example.

**You can always print attrs using `python setup.py print_attrs`**

