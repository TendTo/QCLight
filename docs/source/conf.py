# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import sys

sys.path.insert(
    0, os.path.abspath("../../src/qclight")
)  # path to the actual project root folder

project = "QCLight"
copyright = "2022, TendTo"
author = "TendTo"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # read documentation from the comments
    "sphinx.ext.napoleon",  # to use NumPy and Google style docstrings
    "sphinx.ext.githubpages",  # generates the .nojekyll file
    "sphinx.ext.viewcode",  # add source code links to the documentation
    "sphinx_rtd_dark_mode",  # dark mode for ReadTheDocs
    "sphinx_autodoc_typehints",  # improves the type hinting
]

templates_path = ["_templates"]
exclude_patterns: "list[str]" = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_favicon = "_static/img/logo.svg"
html_logo = "_static/img/logo.svg"
html_css_files = [
    "css/dark.css",
]
html_context = {
    "display_github": True,
    "github_user": "TendTo",
    "github_repo": "QCLight",
    "github_version": "master/docs/source/",
}

# -- Extension configuration -------------------------------------------------

# Configuration of "sphinx_autodoc_typehints"
typehints_use_rtype = False
typehints_defaults = "comma"


def setup(app):
    from sphinx.ext.autodoc import between

    app.connect("autodoc-process-docstring", between("```", exclude=True))
    app.connect("autodoc-process-docstring", between(r"\|(\s*\S+\s*\|)+", exclude=True))
