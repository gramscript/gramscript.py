Available Methods
=================

This page is about gramscript methods. All the methods listed here are bound to a :class:`~gramscript.Client` instance,
except for :meth:`~gramscript.idle()`, which is a special function that can be found in the main package directly.

.. code-block:: python
    :emphasize-lines: 6

    from gramscript import Client

    app = Client("my_account")

    with app:
        app.send_message("haskell", "hi")

.. contents:: Contents
    :backlinks: none
    :local:

-----

.. currentmodule:: gramscript.Client

Utilities
---------

.. autosummary::
    :nosignatures:

    {utilities}

.. toctree::
    :hidden:

    {utilities}

.. currentmodule:: gramscript

.. autosummary::
    :nosignatures:

    idle

.. toctree::
    :hidden:

    idle

.. currentmodule:: gramscript.Client

Messages
--------

.. autosummary::
    :nosignatures:

    {messages}

.. toctree::
    :hidden:

    {messages}

Chats
-----

.. autosummary::
    :nosignatures:

    {chats}

.. toctree::
    :hidden:

    {chats}

Users
-----

.. autosummary::
    :nosignatures:

    {users}

.. toctree::
    :hidden:

    {users}

Contacts
--------

.. autosummary::
    :nosignatures:

    {contacts}

.. toctree::
    :hidden:

    {contacts}

Password
--------

.. autosummary::
    :nosignatures:

    {password}

.. toctree::
    :hidden:

    {password}

Bots
----

.. autosummary::
    :nosignatures:

    {bots}

.. toctree::
    :hidden:

    {bots}

Authorization
-------------

.. autosummary::
    :nosignatures:

    {authorization}

.. toctree::
    :hidden:

    {authorization}

Advanced
--------

Methods used only when dealing with the raw Telegram API.
Learn more about how to use the raw API at :doc:`Advanced Usage <../../topics/advanced-usage>`.

.. autosummary::
    :nosignatures:

    {advanced}

.. toctree::
    :hidden:

    {advanced}