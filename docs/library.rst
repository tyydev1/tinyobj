Library Documentation
=====================

Installation
------------

Install the library using pip:

.. code-block:: bash

   pip install tobj

API Reference
-------------

tobj.load(file)
~~~~~~~~~~~~~~~

Loads a TOBJ file and returns a Python dictionary.

**Example:**

.. code-block:: python

   import tobj

   with open("data.tobj", "r") as f:
       data = tobj.load(f)
   print(data)

tobj.dump(data, file)
~~~~~~~~~~~~~~~~~~~~

Writes a Python dictionary to a TOBJ file.

**Example:**

.. code-block:: python

   import tobj

   data = {"User": {"name": "Alice", "age": 30}}
   with open("user.tobj", "w") as f:
       tobj.dump(data, f)

Usage Examples
--------------

Reading a TOBJ File
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tobj

   with open("config.tobj", "r") as f:
       config = tobj.load(f)
   print(config["User"]["name"])

Writing a TOBJ File
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tobj

   data = {"User": {"name": "Alice", "age": 30}}
   with open("user.tobj", "w") as f:
       tobj.dump(data, f)
