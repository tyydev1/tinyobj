# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from typing import List


project = 'TinyObj'
copyright = '2025, Razka Rizaldi'
author = 'Razka Rizaldi'
release = '0.2.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions: list[str] = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'autoapi.extension',
]

templates_path = ['_templates']
exclude_patterns: list[str] = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# -- AutoAPI configuration -------------------------------------------------
autoapi_type = 'python'
autoapi_dirs = ['../../tobj']
autoapi_options = [
    'members',
    'undoc-members',
    'show-inheritance',
    'show-module-summary',
    'special-members',
]
autoapi_root = 'api'  # output dir inside docs/ (default: 'autoapi')
autoapi_add_toctree_entry = True
