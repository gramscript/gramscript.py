from gramscript import Client, filters

app = Client("5582426331:AAHEv_idaYL9KWwQTLKXbgy5P23PJnjo7AI")


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply_text(f"Hello {message.from_user.mention}")


app.run()
