# bot/admin_commands.py

from pyrogram import Client, filters
from pyrogram.types import Message
from config import ADMINS
from database.mongo import db

# Set number of media to deliver per user
@Client.on_message(filters.command("setmedia") & filters.user(ADMINS))
async def set_media_count(client: Client, message: Message):
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        return await message.reply("Usage: /setmedia 5")
    await db.set_setting("media_count", int(args[1]))
    await message.reply(f"✅ Media count set to {args[1]}")

# Set delete delay in minutes
@Client.on_message(filters.command("setdelay") & filters.user(ADMINS))
async def set_delete_delay(client: Client, message: Message):
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        return await message.reply("Usage: /setdelay 10")
    await db.set_setting("delete_delay", int(args[1]))
    await message.reply(f"✅ Auto-delete delay set to {args[1]} minutes")

# Set caption (HTML allowed)
@Client.on_message(filters.command("setcaption") & filters.user(ADMINS))
async def set_caption(client: Client, message: Message):
    if len(message.text.split(None, 1)) < 2:
        return await message.reply("Usage: /setcaption <HTML formatted caption>")
    caption = message.text.split(None, 1)[1]
    await db.set_setting("caption", caption)
    await message.reply("✅ Caption has been set.")

# Set inline buttons format
@Client.on_message(filters.command("setbuttons") & filters.user(ADMINS))
async def set_buttons(client: Client, message: Message):
    if len(message.text.split(None, 1)) < 2:
        return await message.reply("Usage: /setbuttons\nButton1=URL1 | Button2=URL2\nButton3=URL3")
    await db.set_setting("buttons", message.text.split(None, 1)[1])
    await message.reply("✅ Buttons saved.")

# Optional bottom info/help button
@Client.on_message(filters.command("setinfobutton") & filters.user(ADMINS))
async def set_info_button(client: Client, message: Message):
    if len(message.text.split(None, 1)) < 2 or "=" not in message.text:
        return await message.reply("Usage: /setinfobutton Text=https://example.com")
    await db.set_setting("infobutton", message.text.split(None, 1)[1])
    await message.reply("✅ Info button set.")

# Set referral bonus (media per referral)
@Client.on_message(filters.command("setrefreward") & filters.user(ADMINS))
async def set_referral_reward(client: Client, message: Message):
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        return await message.reply("Usage: /setrefreward 2")
    await db.set_setting("ref_bonus", int(args[1]))
    await message.reply(f"✅ Referral reward set to {args[1]} media per user")

# Set cap on referral rewards
@Client.on_message(filters.command("setrefcap") & filters.user(ADMINS))
async def set_referral_cap(client: Client, message: Message):
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        return await message.reply("Usage: /setrefcap 20")
    await db.set_setting("ref_cap", int(args[1]))
    await message.reply(f"✅ Referral cap set to {args[1]} media")

# Set hours between user accesses
@Client.on_message(filters.command("setcooldown") & filters.user(ADMINS))
async def set_cooldown(client: Client, message: Message):
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        return await message.reply("Usage: /setcooldown 8")
    await db.set_setting("cooldown_hours", int(args[1]))
    await message.reply(f"✅ Cooldown time set to {args[1]} hours")
