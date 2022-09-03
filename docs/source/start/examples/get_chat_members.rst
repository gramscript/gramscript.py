get_chat_members
================

This example shows how to get all the members of a chat.

.. code-block:: python

    from gramscript import Client

    app = Client("my_account")
    target = "gramscriptchat"  # Target channel/supergroup

    with app:
        for member in app.iter_chat_members(target):
            print(member.user.first_name)