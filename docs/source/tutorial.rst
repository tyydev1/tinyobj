Tutorial: Getting Started with TinyObj
======================================

TinyObj (TOBJ) is a minimalist, human-readable data format designed for "freedom." It uses a simple shorthand to represent nested objects, properties, and lists without the heavy nesting of JSON or the indentation-sensitivity of YAML.

Syntax Basics
-------------

There are three primary symbols in TinyObj:

* ``*`` (Star): Defines an **Object** or a path to an object.
* ``>`` (Arrow): Defines a **Property** (key-value pair).
* ``-`` (Dash): Defines a **List Item**.

Sub-symbols include:

* Dot (``.``): Used in object names to denote nested objects (e.g., ``*User.profile``).
* Octothorpe (``#``): Used for comments. Anything after ``#`` on a line is ignored.
* Double Slash (``//``): Also used for comments.
* Ellipsis (``...``): Used to indicate continuation. Is ignored during parsing, and only the ellipsis. (anything else on the line is parsed)

Basic comments
~~~~~~~~~~~~~~

Comments can be added using ``#`` or ``//``. Anything following these symbols on the same line is ignored.

.. code-block:: tobj

    *User  # This is a user object
      > name "Alice"  // User's name
      > age 30  # User's age

There's also the ellipsis symbol ``...`` which indicates continuation, but should not be used for comments or on production.

.. code-block:: tobj

    *Data
        > values
            - 10
            - 20
            - 30
        ...  # TEAM NOTE: More values can be added here
        // DOC NOTE: Ellipsis shouldn't be used for comments and production code.


Basic Object
~~~~~~~~~~~~

An object starts with a ``*`` followed by its name. Properties belong to the most recently declared object.

.. code-block:: tobj

    *User
        > name    "Alice"
        > age     30
        > active  true

This translates to the following Python dictionary:
``{"User": {"name": "Alice", "age": 30, "active": True}}``

Nested Objects
~~~~~~~~~~~~~~

You can define nested structures using dot notation. You do not need to define the parent object explicitly first; TinyObj will create the path for you.

.. code-block:: tobj

    *User.profile
        > bio       "Software Engineer"
        > location  "Earth"

Lists and Collections
~~~~~~~~~~~~~~~~~~~~~

Lists can be written in two ways:

1.  **Multi-line lists**: Place each item on a new line starting with a ``-``.
2.  **One-liner lists**: Place items on the same line as the property.

.. code-block:: tobj

    *Config
        > tags
            - python
            - rust
            - tobj

    *Data
        > readings - 10 - 20 - 30.5


Using the Python API
--------------------

The ``tobj`` package provides a simple interface similar to Python's built-in ``json`` module.

Loading TinyObj
~~~~~~~~~~~~~~~

You can parse TinyObj from a string or a file using ``loads`` and ``load``.

.. code-block:: python

    import tobj

    data = """
    *Settings
    > theme "dark"
    > volume 80
    """

    # Parse from string
    config = tobj.loads(data)
    print(config['Settings']['theme']) # Output: dark

    # Parse from file
    with open('config.tobj', 'r') as f:
        config_file = tobj.load(f)

Serializing to TinyObj
~~~~~~~~~~~~~~~~~~~~~~

To convert a Python dictionary back into TinyObj format, use ``dumps`` or ``dump``.

.. code-block:: python

    import tobj

    my_data = {
        "Database": {
            "host": "localhost",
            "ports": [8080, 8081]
        }
    }

    tobj_string = tobj.dumps(my_data)
    print(tobj_string)

Handling Errors
---------------

TinyObj provides descriptive error messages that highlight exactly where a syntax error occurred using carets (``^``).

.. code-block:: python

    try:
        tobj.loads("> name Alice") # Error: Property without object context
    except Exception as e:
        print(e)

Common Data Types
-----------------

TinyObj supports the following types natively:

* **Strings**: ``"Hello"`` (Supports escapes like ``\n``, ``\t``, ``\"``)
* **Numbers**: ``42``, ``-3.14``
* **Booleans**: ``true``, ``false``
* **Nulls**: ``nothing``
* **Identifiers**: Unquoted keys and values (e.g., ``Alice``)

Next Steps
----------

* Explore the **API Reference** for details on the Lexer and Parser.
* Check out the ``samples/`` directory in the repository for more complex examples.