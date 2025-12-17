TOBJ Syntax Guide
=================

TOBJ is a lightweight data format designed for simplicity and readability.

Basic Syntax
------------

Objects
~~~~~~~

Objects start with ``*`` followed by the object name.

**Example:**

.. code-block:: tobj

   *User

Properties
~~~~~~~~~~

Properties are defined using ``>`` followed by the key and value.

**Example:**

.. code-block:: tobj

   *User
       > name Alice
       > age 30

Comments
~~~~~~~~

Comments can be added using ``#`` or ``//``.

**Example:**

.. code-block:: tobj

   *User
       > name Alice  # This is a comment
       > age 30      // This is also a comment

Lists
~~~~~

Lists are defined using ``-`` for each item.

**Example:**

.. code-block:: tobj

   *User
       > hobbies
           - Reading
           - Gaming
           - Hiking

Strings
~~~~~~~

Strings can be wrapped in quotes.

**Example:**

.. code-block:: tobj

   *User
       > bio "Hello, world!"

Special Keywords
~~~~~~~~~~~~~~~

- ``true`` for boolean true.
- ``false`` for boolean false.
- ``nothing`` for null values.

**Example:**

.. code-block:: tobj

   *User
       > active true
       > pet nothing

Example TOBJ File
-----------------

.. code-block:: tobj

   *$
   > key ctrl+alt+c
   > action "Suspend Machine"
   > timeout 10

   *User
       > name Alice
       > age 30
       > active true
       > hobbies
           - Reading
           - Gaming
           - Hiking
