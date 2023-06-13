"""Configuration file for the Sphinx documentation builder."""
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import toml

with open("../pyproject.toml") as f:
    data = toml.load(f)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "LanguageAssistant"
copyright = "2023, Daniel Gleaves"  # noqa: A001
author = "Daniel Gleaves"

version = data["tool"]["poetry"]["version"]
release = version

html_title = project + " " + version
html_last_updated_fmt = "%b %d, %Y"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autodoc.typehints",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinxcontrib.autodoc_pydantic",
    # "myst_nb",
    "sphinx_copybutton",
    # "sphinx_panels",
    "IPython.sphinxext.ipython_console_highlighting",
]
source_suffix = [".ipynb", ".html", ".md", ".rst"]

autosummary_generate = True  # Turn on sphinx.ext.autosummary
autoclass_content = "both"  # Add __init__ doc (ie. params) to class summaries
html_show_sourcelink = (
    False  # Remove 'view source code' from top of page (for html, not python)
)
autodoc_inherit_docstrings = True  # If no docstring, inherit from base class
add_module_names = False  # Remove namespaces from class/method signatures

# Autodoc Pydantic
autodoc_pydantic_model_show_json = False
autodoc_pydantic_field_list_validators = False
autodoc_pydantic_config_members = False
autodoc_pydantic_model_show_config_summary = False
autodoc_pydantic_model_show_validator_members = False
autodoc_pydantic_model_show_field_summary = False
autodoc_pydantic_model_members = False
autodoc_pydantic_model_undoc_members = False
# autodoc_typehints = "signature"
# autodoc_typehints = "description"

# Type hints
typehints_fully_qualified = False
always_document_param_types = False
typehints_document_rtype = True
typehints_use_rtype = True
typehints_defaults = "braces-after"
simplify_optional_unions = False
typehints_formatter = None

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = ["_static"]

html_theme_options = {
    "path_to_docs": "docs",
    "repository_url": "https://github.com/dagleaves/languageassistant",
    "use_repository_button": True,
}

html_context = {
    "display_github": True,  # Integrate GitHub
    "github_user": "dagleaves",  # Username
    "github_repo": "languageassistant",  # Repo name
    "github_version": "main",  # Version
    "doc_path": "/docs/",  # Path in the checkout to the docs root
}
