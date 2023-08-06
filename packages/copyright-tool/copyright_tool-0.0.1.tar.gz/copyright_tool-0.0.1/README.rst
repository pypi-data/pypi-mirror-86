=========
copyright_tool
=========


.. image:: https://img.shields.io/pypi/v/copyright_tool.svg
        :target: https://pypi.python.org/pypi/copyright_tool

.. image:: https://img.shields.io/gitlab/pipeline/pennatus/copyright_tool/master
        :alt: Gitlab pipeline status

.. image:: https://readthedocs.org/projects/copyright_tool/badge/?version=latest
        :target: https://copyright_tool.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Use to automatically scan all tracked files in your git repository and add/update the
copyright.

Simply create files like `.copyright.py.tpl` at the root of your folder that are commented
as dictated by the language:

```
####################################
Copyright {year} Pennatus
####################################
```

You can create a different `.copyright.<language>.tpl` for each type of source file.

To exclude files, create a file called `.copyrightignore` at the root of your folder using
syntax similar to your `.gitignore` to specify files to exclude from the search process.

* Free software: MIT license
* Documentation: https://copyright_tool.readthedocs.io.


Features
--------

* Reads environment secrets from a KV-2 path and outputs a .env file.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
