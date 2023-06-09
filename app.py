from pyrogram import Client, filters, idle
from pyrogram.types import Message
import psutil
import os

ADMIN = os.environ.get("ADMIN") or 799041666
API_ID   = os.environ.get("API_ID") or 1167061
API_HASH = os.environ.get("API_HASH") or "4de49642ae630ae385b6c10faa7155be"

proxy = {
    "scheme": "socks5",
    "hostname": "localhost",
    "port": 9150,
    "username": "1",
    "password": "1",
}
tor = os.environ.get("TOR") or None
if tor == "True":
   tor = proxy

app = Client("self-bot", API_ID, API_HASH, proxy=tor)

@app.on_message(filters.user(ADMIN))
async def main(client: Client, message: Message):
    text    = message.text
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    handlers = {
        "/save": save_message,
        "/ping": ping_server,
   }
    if text in handlers.keys():
        command = text
        await handlers[command](client, message)

async def save_message(client: Client, message: Message):
    user_id = message.from_user.id
    reply_message = message.reply_to_message

    if reply_message.text:
        text = reply_message.text
        
        await client.send_message(user_id, text)

    else:
        media      = await reply_message.download(in_memory=True)
        media_type = reply_message.media.value
        caption    = reply_message.caption
        command    = f"send_{media_type}"
        send_func  = getattr(client, command)
        await send_func(user_id, media, caption=caption)
            
    await message.edit_text("`message has been saved in your Saved Messages!`")

async def ping_server(client: Client, message: Message):
    process = psutil.Process()
    memory_info = process.memory_info().rss  # in bytes
    memory_mb = memory_info / (1024 ** 2)  # convert to MB
    memory_total = psutil.virtual_memory().total / (1024 ** 2)
    
    await message.edit_text(f"`status: online\nmemory total: {memory_total:.2f}\nmemory usage: {memory_mb:.2f} MB`")
    
    
app.start(); print("self is running..."); idle()
app.stop()