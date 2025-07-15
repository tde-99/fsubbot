# bot/media_indexer.py

from pyrogram import Client, filters
from pyrogram.types import Message
from config import ADMINS, MEDIA_CHANNEL
from database.mongo import db

@Client.on_message(filters.command("setmedia") & filters.user(ADMINS))
async def set_media_pool(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("❗ Please reply to a media message from your media channel.")

    reply = message.reply_to_message
    if reply.chat.id != MEDIA_CHANNEL:
        return await message.reply("❌ That message is not from the configured media channel.")

    msg_id = reply.message_id
    await db.add_media(msg_id)
    await message.reply(f"✅ Media saved to pool (ID: <code>{msg_id}</code>)")
