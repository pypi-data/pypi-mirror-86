sphinx-nextstrain-theme
=======================

A `Sphinx theme`_ for Nextstrain's documentation, based on `Read The Docs`_'
default theme (sphinx_rtd_theme_).

Installation
------------

This theme is distributed on PyPI as nextstrain-sphinx-theme_ and can be
installed with ``pip``:

.. code:: console

    $ python3 -m pip install nextstrain-sphinx-theme

To use the theme in your Sphinx project, you will need to add the following to
your ``conf.py`` file:

.. code:: python

    html_theme = "nextstrain-sphinx-theme"

This theme is based on sphinx_rtd_theme_ and accepts all of the same
`configuration options`_ settable via ``html_theme_option``.  One additional
option is supported:

:logo: Boolean determining if the Nextstrain logo should be displayed.
       Defaults to true.

If your project wants to display its own logo, just set Sphinx's ``html_logo``
to point to the image file in your Sphinx project.

.. code:: python

    html_logo = "_static/your-logo.png"

This will automatically take precedence over the default Nextstrain logo
provided by the theme.

Releasing
---------

1. Make sure you have a PyPI account and access to https://pypi.org/project/nextstrain-sphinx-theme/.
2. Make sure all your changes have been commited to the ``main`` branch.
3. Add a commit which describes the changes from the previous version to ``CHANGES.md`` and updates the version number in ``lib/nextstrain/sphinx/theme/VERSION``.
4. Tag this commit with the version number, e.g. ``git tag -a 2020.4 -m "version 2020.4"``.
5. Push the commit and the tag to the ``main`` branch.
6. `Generate the source and binary distributions with setup.py <https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives>`__.
7. `Upload the two files from step 3 to PyPI with twine <https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives>`__.

.. _Sphinx theme: https://www.sphinx-doc.org/en/master/theming.html
.. _Read The Docs: https://readthedocs.org
.. _sphinx_rtd_theme: https://github.com/readthedocs/sphinx_rtd_theme
.. _nextstrain-sphinx-theme: https://pypi.org/project/nextstrain-sphinx-theme/
.. _configuration options: https://sphinx-rtd-theme.readthedocs.io/en/latest/configuring.html
