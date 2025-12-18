.. TinyObj documentation master file, created by
   sphinx-quickstart on Thu Dec 18 13:52:38 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TinyObj documentation
=====================

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   tutorial
   api/tobj


**TinyObj** is a minimal, human-readable object notation designed for configuration,
data exchange, and structured text. It uses simple sigils to define objects (``*``),
properties (``>``), and lists (``-``), making it easy to write by hand and parse
programmatically.


.. code-block:: tobj

    *User
      > name    "Alice"
      > age     30
      > tags
         - python
         - rust

    *User.profile
      > active    true
      > score     9001

Key features:

- **Hierarchical objects** via dot-separated paths (e.g., ``*User.profile``)
- **Typed values**: strings, numbers, booleans, ``nothing`` (null), and lists
- **Clean, indentation-free syntax**
- **Built-in error reporting** with source positions and visual highlights
- **Bi-directional**: parse to Python dict, serialize back to TinyObj

This documentation includes:

- A :doc:`tutorial <tutorial>` for getting started
- A full :doc:`api/tobj` reference for developers
- Examples and best practices for real-world usage

Get started by installing TinyObj:

.. code-block:: bash

    pip install tobj

Then use it in Python:

.. code-block:: python

    import tobj
    data = tobj.loads("*Config >debug true")
    print(data)  # {'Config': {'debug': True}}

Check out the TOBJ repository on `GitHub <https://github.com/tyydev1/tinyobj>`_ for source code, examples, and more information.
It's also online on PyPI: `https://pypi.org/project/tobj/ <https://pypi.org/project/tobj/>`_.

