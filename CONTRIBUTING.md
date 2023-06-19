# LanguageAssistant contributing guide

## Getting started

If you encounter a bug or have a suggestion, please make an issue describing any problems, possible solutions, and any
other details that may be useful.

If you have programming experience, feel free to make a pull request with proposed additions or changes.

---

## Development

### Local setup

* Fork this repository
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

Anything run through the `poetry run` command is run this way to use the poetry plugin to load environment variables
from a .env file. You may choose to load the variables a different way and may omit the `poetry run` portion.


### Making changes

* Create a new branch for your changes
* Make your local commits and push to your branch
* Make a pull request on this repository
  * Link to any relevant open issues to your PR
  * Describe the changes you made and, if not explained in an issue, why they are necessary or beneficial

### Pre-commit checks

Before a pull request may be merged, it must pass all checks, including auto-formatters
(e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), tests, and other quality checks to make sure the changes are good
before a commit/push happens.

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

## Testing

If you add or change any of the functional code in the repository, be sure to add tests to ensure your code is covered.
If any tests fail, be sure to try and fix the issue if you are able.

To run the tests locally, run

```sh
poetry run pytest
```

To run a specific test,

```sh
poetry run pytest tests.test_subdirectory.test_module.test_specific_function
```

---

## Documentation

The documentation is automatically generated from the content of the docs directory and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [GitHub project page
 ](https://pages.github.com/) automatically as part each release.

To generate a local copy of the docs, run

```sh
cd docs
poetry run make html
```
