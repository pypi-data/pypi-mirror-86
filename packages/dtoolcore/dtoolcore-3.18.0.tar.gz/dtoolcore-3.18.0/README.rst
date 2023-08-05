Manage scientific data sets
===========================


.. image:: https://badge.fury.io/py/dtoolcore.svg
   :target: http://badge.fury.io/py/dtoolcore
   :alt: PyPi package

.. image:: https://travis-ci.org/jic-dtool/dtoolcore.svg?branch=master
   :target: https://travis-ci.org/jic-dtool/dtoolcore
   :alt: Travis CI build status (Linux)

.. image:: https://ci.appveyor.com/api/projects/status/ifd8qrfidslvs4i3?svg=true
   :target: https://ci.appveyor.com/project/tjelvar-olsson/dtoolcore
   :alt: AppVeyor CI build status (Windows)

.. image:: https://codecov.io/github/jic-dtool/dtoolcore/coverage.svg?branch=master
   :target: https://codecov.io/github/jic-dtool/dtoolcore?branch=master
   :alt: Code Coverage

.. image:: https://readthedocs.org/projects/dtoolcore/badge/?version=latest
   :target: https://readthedocs.org/projects/dtoolcore?badge=latest
   :alt: Documentation Status

- Documentation: http://dtoolcore.readthedocs.io
- GitHub: https://github.com/jic-dtool/dtoolcore
- PyPI: https://pypi.python.org/pypi/dtoolcore
- Free software: MIT License

Features
--------

- Core API for adding different types of metadata to files on disk
- Automatic generation of structural metadata
- Programmatic discovery and access of items in a dataset
- Structural metadata includes hash, size and modification time for
  subsequent integrity checks
- Ability to annotate individual files with arbitrary metadata
- Metadata stored on disk as plain text files, i.e. disk datasets
  generated using this API can be accessed without special tools
- Ability to create plugins for custom storage solutions
- Plugins for iRODS and Microsoft Azure storage backends available
- Cross-platform: Linux, Mac and Windows are all supported
- Works with Python 2.7, 3.5 and 3.6
- No external dependencies

Overview
--------

The dtoolcore project provides a Python API for managing (scientific) data.
It allows researchers to:

- Package data and metadata into a dataset
- Organise and backup datasets easily
- Find datasets of interest
- Verify the contents of datasets
- Discover and work with data programatically
