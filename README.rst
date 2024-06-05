PyWorkbench examples
####################

|pyansys| |GH-CI|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?labelColor=black&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |GH-CI| image:: https://github.com/ansys-internal/pyworkbench-examples/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys/pyworkbench-examples/actions/workflows/ci_cd.yml
   :alt: GH-CI


About
=====

PyWorkbench examples is a repository containing a plethora of showcases on how
to use the `PyWorkbench`_ library. PyWorkbench is a Python library that provides
a simple and intuitive way to create and manage simulation workflows over Ansys
products.

Documentation
=============

The `official examples`_ contains the following chapters:

- `Basic examples`_: A collection of basic examples that showcase the basic
  functionalities of PyWorkbench.

- `Advanced examples`_: A collection of advanced examples that showcase the
  more complex functionalities of PyWorkbench.

Additionally, you can build the documentation locally by following the steps:

1. Install `Tox`_ in your local environment by running ``python -m pip install
   tox``
2. Build the documentation by running ``tox -e doc-html``

Troubleshooting
===============

For troubleshooting or reporting issues, please open an issue in the project
repository.

Please follow these steps to report an issue:

- Go to the project repository.
- Click on the ``Issues`` tab.
- Click on the ``New Issue`` button.
- Provide a clear and detailed description of the issue you are facing.
- Include any relevant error messages, code snippets, or screenshots.

Additionally, you can refer to the `PyWorkbench documentation`_ for additional
resources and troubleshooting guides.

License
=======

You can find the full text of the license in the `LICENSE <LICENSE>`_ file.


.. Links and references

.. _Tox: https://tox.wiki/en/stable/

.. _PyWorkbench: https://github.com/ansys/pyworkbench

.. _official examples: https://examples.workbench.docs.pyansys.com
.. _Basic examples: https://examples.workbench.docs.pyansys.com/version/dev/basic-examples/index.html
.. _Advanced examples: https://examples.workbench.docs.pyansys.com/version/dev/advanced-examples/index.html
.. _PyWorkbench documentation: https://workbench.docs.pyansys.com
