Install Guide
=============

Being a modern Python library, **gramscript** requires Python 3.6+ to be installed in your system.
We recommend using the latest versions of both Python 3 and pip.

- Get **Python 3** from https://www.python.org/downloads/ (or with your package manager).
- Get **pip** by following the instructions at https://pip.pypa.io/en/latest/installing/.

.. important::

    gramscript supports **Python 3** only, starting from version 3.6. **PyPy** is supported too.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Install gramscript
----------------

-   The easiest way to install and upgrade gramscript to its latest stable version is by using **pip**:

    .. code-block:: text

        $ pip3 install -U gramscript

-   or, with :doc:`TgCrypto <../topics/tgcrypto>` as extra requirement (recommended):

    .. code-block:: text

        $ pip3 install -U gramscript tgcrypto

Bleeding Edge
-------------

gramscript is always evolving, although new releases on PyPI are published only when enough changes are added, but this
doesn't mean you can't try new features right now!

In case you'd like to try out the latest gramscript features, the `GitHub repo`_ is always kept updated with new changes;
you can install the development version straight from the ``master`` branch using this command (note "master.zip" in
the link):

.. code-block:: text

    $ pip3 install -U https://github.com/gramscript/gramscript/archive/master.zip

Verifying
---------

To verify that gramscript is correctly installed, open a Python shell and import it.
If no error shows up you are good to go.

.. parsed-literal::

    >>> import gramscript
    >>> gramscript.__version__
    '|version|'

.. _`Github repo`: http://github.com/gramscript/gramscript
