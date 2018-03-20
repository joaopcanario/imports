Imports

.. image:: https://img.shields.io/pypi/v/imports.svg
        :target: https://pypi.python.org/pypi/imports

.. image:: https://img.shields.io/travis/joaopcanario/imports.svg
        :target: https://travis-ci.org/joaopcanario/imports

.. image:: https://readthedocs.org/projects/imports/badge/?version=latest
        :target: https://imports.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

A helper tool to identify the unused installed packages that are listed on requirements.txt


* Free software: MIT license
* Documentation: https://imports.readthedocs.io.


Features
--------


> __WARNING:__ Remove packages listed by this tool helper it's at your own risk

## Usage

> NOTE: Before start, it's expected that there is a `requirements.txt` file on the project root folder and your virtualenv is active as well.

Download `imports.py` and use the command below passing the path to the root folder of project that'll be checked. After that, the helper will list all the possible packages that aren't being used in your project:

```python
imports PATH_TO_PROJECT_FOLDER
```

After this, I suggest the use of [pip-autoremove package](https://github.com/invl/pip-autoremove) to uninstall the wrong entries listed.


Here a small example:

![Input](https://github.com/joaopcanario/imports/blob/master/media/entry.png)

the output:

![Output](https://github.com/joaopcanario/imports/blob/master/media/output.png)


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
