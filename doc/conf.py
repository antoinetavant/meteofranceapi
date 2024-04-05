# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import meteofrance_publicapi

project = "meteofrance_publicapi"
copyright = "2024, Antoine Tavant"
author = "Antoine Tavant"
version = meteofrance_publicapi.__version__
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    #"sphinx_gallery.gen_gallery",
    "sphinx_design",
    "nbsphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "en"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "github_url": "https://github.com/antoinetavant/meteofranceapi",
    "announcement": "<p>This is a Work In Progress project! Things can break without notice!</p>",
}
html_static_path = ["_static"]
html_sidebars = {
    # "**": ["search-field.html", "sidebar-nav-bs.html", 'globaltoc.html',]
    "**": ["search-field.html", "sidebar-nav-bs.html"]
}
# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

html_title = f"{project} v{version} Manual"


# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True

# -- sphinx_gallery Extension configuration -------------------------------------------------
# The path to these directories should be relative to the doc/conf.py file.
sphinx_gallery_conf = {
    "examples_dirs": "../examples",  # path to your example scripts
    "gallery_dirs": "auto_examples",  # path to where to save gallery generated output
    "filename_pattern": "/plot_",  # execute every python script named plot_*.py
    "thumbnail_size": (
        500,
        380,
    ),  # size of the generated thumbnail (the disply param is in the CSS file)
}


# -- nbsphinx extension configuration ----------------------------------------
nbsphinx_execute = "never"  # never, always, or auto (only run if no output available)

# -- Extension configuration -------------------------------------------------
napoleon_use_rtype = False  # move return type inline
