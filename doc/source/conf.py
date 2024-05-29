"""Sphinx documentation configuration file."""

from datetime import datetime
import os
import pathlib
import shutil

import sphinx
from sphinx.util import logging
from sphinx.util.display import status_iterator

from ansys_sphinx_theme import pyansys_logo_black as logo


# Project information
project = "pymechanical-multiworkflow-examples"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "ANSYS, Inc."
release = version = "0.1.dev0"
cname = os.getenv("DOCUMENTATION_CNAME", "docs.pyansys.com")

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Sphinx extensions
extensions = [
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx_design",
    "sphinx_jinja",
    "numpydoc",
    "nbsphinx",
    "myst_parser",
]


templates_path = ['_templates']
exclude_examples = []
exclude_patterns = ["conf.py", "scripts"]

print(f"EXCLUDE_PATTERNS: {exclude_patterns}")

source_suffix = {
    ".rst": "restructuredtext",
    ".mystnb": "jupyter_notebook",
    ".md": "markdown",
}


# -- Options for HTML output -------------------------------------------------

# Select desired logo, theme, and declare the html title
html_logo = logo
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "PyWorkbench Examples"

# specify the location of your github repo
html_theme_options = {
    "github_url": "https://github.com/ansys/pyworkbench-examples",
    "show_prev_next": True,
    "show_breadcrumbs": True,
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
}

# Configuration for nbsphinx
nbsphinx_execute = "always"
nbsphinx_custom_formats = {
    ".mystnb": ["jupytext.reads", {"fmt": "mystnb"}],
    ".py": ["jupytext.reads", {"fmt": ""}],
}
nbsphinx_prompt_width = ""


# -- Sphinx application setup ------------------------------------------------

def copy_examples_dir_to_source_dir(app: sphinx.application.Sphinx):
    """
    Copy the examples directory to the source directory of the documentation.

    Parameters
    ----------
    app : sphinx.application.Sphinx
        Sphinx application instance containing the all the doc build configuration.

    """
    SOURCE_EXAMPLES = pathlib.Path(app.srcdir) / "examples"
    if not SOURCE_EXAMPLES.exists():
        SOURCE_EXAMPLES.mkdir(parents=True, exist_ok=True)

    EXAMPLES_DIRECTORY = SOURCE_EXAMPLES.parent.parent.parent / "examples"

    shutil.copytree(EXAMPLES_DIRECTORY, SOURCE_EXAMPLES, dirs_exist_ok=True)

def copy_examples_to_output_dir(app: sphinx.application.Sphinx, exception: Exception):
    """
    Copy the examples directory to the output directory of the documentation.

    Parameters
    ----------
    app : sphinx.application.Sphinx
        Sphinx application instance containing the all the doc build configuration.
    exception : Exception
        Exception encountered during the building of the documentation.

    """
    OUTPUT_EXAMPLES = pathlib.Path(app.outdir)
    if not OUTPUT_EXAMPLES.exists():
        OUTPUT_EXAMPLES.mkdir(parents=True, exist_ok=True)

    # TODO: investigate why if using:
    #
    # EXAMPLES_DIRECTORY = OUTPUT_EXAMPLES.parent.parent.parent / "examples"
    #
    # blocks Sphinx from finding the Python examples even if the path is the
    # right one. Using SOURCE_EXAMPLES is a workaround to this issue.
    SOURCE_EXAMPLES = pathlib.Path(app.srcdir) / "examples"
    EXAMPLES_DIRECTORY = SOURCE_EXAMPLES.parent.parent.parent / "examples"

    all_examples = list(EXAMPLES_DIRECTORY.glob("**/*.py"))
    examples = [file for file in all_examples if f"{file.name}" not in exclude_examples]

    for file in status_iterator(
            examples, 
            f"Copying example to doc/_build/{app.builder.name}/",
            "green", 
            len(examples),
            verbosity=1,
            stringify_func=(lambda x: x.name),
    ):
        destination_file = OUTPUT_EXAMPLES / file.name
        destination_file.write_text(file.read_text())
    

def remove_examples_from_source_dir(app: sphinx.application.Sphinx, exception: Exception):
    """
    Remove the example files from the documentation source directory.

    Parameters
    ----------
    app : sphinx.application.Sphinx
        Sphinx application instance containing the all the doc build configuration.
    exception : Exception
        Exception encountered during the building of the documentation.

    """
    EXAMPLES_DIRECTORY = pathlib.Path(app.srcdir) / "examples"
    logger = logging.getLogger(__name__)
    logger.info(f"\nRemoving {EXAMPLES_DIRECTORY} directory...")
    shutil.rmtree(EXAMPLES_DIRECTORY)

def setup(app: sphinx.application.Sphinx):
    """
    Run different hook functions during the documentation build.

    Parameters
    ----------
    app : sphinx.application.Sphinx
        Sphinx application instance containing the all the doc build configuration.

    """
    # HACK: rST files are copied to the doc/source directory before the build.
    # Sphinx needs all source files to be in the source directory to build.
    # However, the examples are desired to be kept in the root directory. Once the
    # build has completed, no matter its success, the examples are removed from
    # the source directory.
    app.connect("builder-inited", copy_examples_dir_to_source_dir)
    #app.connect("build-finished", remove_examples_from_source_dir)
    app.connect("build-finished", copy_examples_to_output_dir)
