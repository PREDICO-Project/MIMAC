# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

sys.path.insert(0, os.path.abspath(".."))
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'MIMAC'
copyright = '2024, Francisco Rafael Lozano Martínez, Víctor Sánchez Lara, Carlos Huerga Cabrerizo, Luis Carlos Martínez Gómez and Diego García Pinto'
author = 'Francisco Rafael Lozano Martínez & Víctor Sánchez Lara'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.todo",
              "sphinx.ext.viewcode",
              "sphinx.ext.autodoc",
              'sphinx.ext.napoleon',
              'sphinx.ext.coverage',
              'sphinx.ext.mathjax',
              'nbsphinx',
              "sphinx.ext.githubpages",]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'property-doc-from-class': True,
}

autodoc_member_order = 'bysource'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_logo = "_static/logo.png"
html_theme_options = {
    'logo_only': True,
    'display_version': False,
}

