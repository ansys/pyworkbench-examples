"""Sphinx documentation configuration file."""

from datetime import datetime
import os
import pathlib
import shutil
from typing import List

import sphinx
from sphinx.util import logging
from sphinx.util.display import status_iterator

from ansys_sphinx_theme import get_version_match


# Project information
project = "pymechanical-multiworkflow-examples"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "ANSYS, Inc."

# Read version from VERSION file in base root directory
source_dir = pathlib.Path(__file__).parent.resolve().absolute()
version_file = source_dir / "../../VERSION"
with open(str(version_file), "r") as file:
    __version__ = file.read().splitlines()[0]
release = version = __version__

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
exclude_examples = ["grantami-integration", "pymechanical-integration", "axisymmetric-rotor"]

exclude_patterns = [
    "conf.py",
    "examples/**/scripts/*.py",
    "examples/grantami-integration/*",
    "examples/logging/alternative_target_dir/*.py",
    "examples/pyfluent-mixing-elbow/*",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".mystnb": "jupyter_notebook",
    ".md": "markdown",
}


# -- Options for HTML output -------------------------------------------------

# Select desired logo, theme, and declare the html title
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "PyWorkbench Examples"

# specify the location of your github repo
html_theme_options = {
    "github_url": "https://github.com/ansys/pyworkbench-examples",
    "show_prev_next": True,
    "show_breadcrumbs": True,
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
        ("PyWorkbench", "https://workbench.docs.pyansys.com/"),
    ],
    "switcher": {
        "json_url": f"https://{cname}/versions.json",
        "version_match": get_version_match(version),
    },
    "logo" : "pyansys",
}

html_static_path = ["_static"]
html_css_files = [
    "css/custom.css"
]

# Configuration for nbsphinx
nbsphinx_execute = "always"
nbsphinx_custom_formats = {
    ".mystnb": ["jupytext.reads", {"fmt": "mystnb"}],
    ".py": ["jupytext.reads", {"fmt": ""}],
}
nbsphinx_allow_errors = False
nbsphinx_prompt_width = ""
nbsphinx_thumbnails = {
    # Basic examples
    "examples/logging/main": "_static/thumbnails/default.png",
    "examples/ansys-fluent-workflow/main": "_static/thumbnails/default.png",
    "examples/pymechanical-integration/main": "_static/thumbnails/default.png",
    "examples/pyfluent-workflow/main": "_static/thumbnails/default.png",
    # Advanced examples
    "examples/cooled-turbine-blade/main": "_static/thumbnails/cooled-turbine-blade.png",
    "examples/cyclic-symmetry-analysis/main": "_static/thumbnails/cyclic-symmetry-analysis.png",
    "examples/axisymmetric-rotor/main": "_static/thumbnails/axisymmetric-rotor.png",
    "examples/ansys-aedt-workflow/main": "_static/thumbnails/ansys-aedt-workflow.png",
}


# -- Sphinx application setup ------------------------------------------------

def copytree(src: pathlib.Path, dst: pathlib.Path, excluded: List[str]):
    """
    Recursively copy a directory tree using pathlib.

    Args:
        src (Path): The source directory to copy from.
        dst (Path): The destination directory to copy to.

    Raises:
        ValueError: If the source is not a directory.
    """
    if not src.is_dir():
        raise ValueError(f"The source {src} is not a directory.")

    # Create the destination directory
    dst.mkdir(parents=True, exist_ok=True)

    # Recursively copy files and subdirectories
    for item in src.iterdir():
        if item.name in excluded:
            continue
        src_item = item
        dst_item = dst / item.name
        if src_item.is_dir():
            copytree(src_item, dst_item, excluded)
        else:
            shutil.copy2(src_item, dst_item)


def copy_examples_dir_to_source_dir(app: sphinx.application.Sphinx):
    """
    Copy the examples directory to the source directory of the documentation.

    Parameters
    ----------
    app : sphinx.application.Sphinx
        Sphinx application instance containing the all the doc build configuration.

    """
    SOURCE_EXAMPLES = pathlib.Path(app.srcdir) / "examples"
    SOURCE_EXAMPLES.mkdir(parents=True, exist_ok=True)

    EXAMPLES_DIRECTORY = SOURCE_EXAMPLES.parent.parent.parent / "examples"

    copytree(EXAMPLES_DIRECTORY, SOURCE_EXAMPLES, exclude_examples)


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
    app.connect("build-finished", remove_examples_from_source_dir)
    app.connect("build-finished", copy_examples_to_output_dir)
