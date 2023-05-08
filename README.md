# LanguageAssistant

[![PyPI](https://img.shields.io/pypi/v/languageassistant?style=flat-square)](https://pypi.python.org/pypi/languageassistant/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/languageassistant?style=flat-square)](https://pypi.python.org/pypi/languageassistant/)
[![PyPI - License](https://img.shields.io/pypi/l/languageassistant?style=flat-square)](https://pypi.python.org/pypi/languageassistant/)


---

**Documentation**: [https://dagleaves.github.io/languageassistant](https://dagleaves.github.io/languageassistant)

**Source Code**: [https://github.com/dagleaves/languageassistant](https://github.com/dagleaves/languageassistant)

**PyPI**: [https://pypi.org/project/languageassistant/](https://pypi.org/project/languageassistant/)

---

An LLM-powered language learning assistant

## Installation

```sh
pip install languageassistant
```

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.8+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
pytest
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [GitHub project page
 ](https://pages.github.com/) automatically as part each release.

### Releasing

Trigger the [Draft release workflow](https://github.com/dagleaves/languageassistant/actions/workflows/draft_release.yml)
(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.

Find the draft release from the
[GitHub releases](https://github.com/dagleaves/languageassistant/releases) and publish it. When
 a release is published, it'll trigger [release](https://github.com/dagleaves/languageassistant/blob/master/.github/workflows/release.yml) workflow which creates PyPI
 release and deploys updated documentation.

### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality
 checks to make sure the changes are good before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---
