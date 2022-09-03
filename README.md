<p align="center">
    <a href="https://github.com/gramscript/gramscript">
        <img src="https://i.imgur.com/BOgY9ai.png" alt="gramscript">
    </a>
    <br>
    <b>Telegram MTProto API Framework for Python</b>
    <br>
    <a href="https://docs.gramscript.org">
        Documentation
    </a>
    •
    <a href="https://github.com/gramscript/gramscript/releases">
        Releases
    </a>
    •
    <a href="https://t.me/gramscript">
        Community
    </a>
</p>

## gramscript

``` python
from gramscript import Client, filters

app = Client("my_account")


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply_text(f"Hello {message.from_user.mention}")


app.run()
```

**gramscript** is a modern, elegant and easy-to-use [Telegram](https://telegram.org/) framework written from the ground up
in Python and C. It enables you to easily create custom apps for both user and bot identities (bot API alternative) via
the [MTProto API](https://docs.gramscript.org/topics/mtproto-vs-botapi).

### Features

- **Easy**: You can install gramscript with pip and start building your applications right away.
- **Elegant**: Low-level details are abstracted and re-presented in a much nicer and easier way.
- **Fast**: Crypto parts are boosted up by [TgCrypto](https://github.com/gramscript/tgcrypto), a high-performance library
  written in pure C.
- **Asynchronous**: Allows both synchronous and asynchronous models to fit all usage needs.
- **Documented**: API methods, types and public interfaces are all [well documented](https://docs.gramscript.org).
- **Type-hinted**: Types and methods are all type-hinted, enabling excellent editor support.
- **Updated**, to make use of the latest Telegram API version and features.
- **Bot API-like**: Similar to the Bot API in its simplicity, but much more powerful and detailed.
- **Pluggable**: The Smart Plugin system allows to write components with minimal boilerplate code.
- **Comprehensive**: Execute any advanced action an official client is able to do, and even more.

### Requirements

- Python 3.6 or higher.
- A [Telegram API key](https://docs.gramscript.org/intro/setup#api-keys).

### Installing

``` bash
pip3 install gramscript
```

### Resources

- The docs contain lots of resources to help you get started with gramscript: https://docs.gramscript.org.
- Seeking extra help? Come join and ask our community: https://t.me/gramscript.
- For other kind of inquiries, you can send a [message](https://t.me/haskell) or an [e-mail](mailto:dan@gramscript.org).

### Copyright & License

- Copyright (C) 2017-2020 Dan <<https://github.com/delivrance>>
- Licensed under the terms of the [MIT License](COPYING.lesser)
