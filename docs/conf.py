# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Path setup --------------------------------------------------------------
# Add the project root so autodoc can find jugaad_data
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
project = 'jugaad-data'
copyright = '2026, jugaad-py'
author = 'jugaad-py'

# The full version, including alpha/beta/rc tags
release = '0.33.1'
version = '0.33'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
    'myst_parser',
]

toc_object_entries = True
toc_object_entries_show_parents = "hide"
add_module_names = False

autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Include __init__ docstrings in autosummary
autodoc_default_flags = ['members']

# -- Options for autodoc -----------------------------------------------------
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'show-inheritance': True,
}

# Napoleon settings (Google-style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False

# -- Options for HTML output -------------------------------------------------
html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']

html_theme_options = {
    'navigation_depth': 3,
    'show_toc_level': 2,
    'navbar_align': 'left',
    'icon_links': [
        {
            'name': 'GitHub',
            'url': 'https://github.com/jugaad-py/jugaad-data',
            'icon': 'fa-brands fa-github',
        },
        {
            'name': 'PyPI',
            'url': 'https://pypi.org/project/jugaad-data/',
            'icon': 'fa-solid fa-box',
        },
    ],
}

# -- Options for intersphinx -------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'requests': ('https://requests.readthedocs.io/en/latest/', None),
}

# -- Copybutton settings -----------------------------------------------------
copybutton_prompt_text = r'>>> |\$ '
copybutton_prompt_is_regexp = True
