# bot/admin_commands.py

from pyromod import Client
from pyrogram import filters
from pyrogram.types import Message
from config import ADMINS
from database.mongo import db

@Client.on_message(filters.command("adminhelp") & filters.user(ADMINS))
async def admin_help(client: Client, message: Message):
    await message.reply(
        "<b>Admin Commands:</b>\n\n"
        "/settings - Open the settings panel\n"
        "/stats - View bot stats\n"
        "/resetuser <user_id> - Reset a user's data\n"
        "/topref - Show top referrers"
    )

@Client.on_message(filters.command("stats") & filters.user(ADMINS))
async def stats(client: Client, message: Message):
    users = await db.get_all_users()
    media = await db.get_media_pool()
    await message.reply(
        f"👥 Total Users: {len(users)}\n"
        f"📦 Media Count: {len(media)}"
    )

@Client.on_message(filters.command("resetuser") & filters.user(ADMINS))
async def reset_user(client: Client, message: Message):
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        return await message.reply("Usage: /resetuser <user_id>")

    user_id = int(args[1])
    await db.db.users.update_one({"_id": user_id}, {"$set": {"referrals": 0, "bonus_used": 0, "last_access": None}})
    await message.reply(f"✅ User {user_id} has been reset.")

@Client.on_message(filters.command("topref") & filters.user(ADMINS))
async def top_referrers(client: Client, message: Message):
    users = await db.db.users.find({"referrals": {"$gt": 0}}).sort("referrals", -1).limit(10).to_list(length=10)
    if not users:
        return await message.reply("No referrers yet.")

    text = "<b>🏆 Top 10 Referrers:</b>\n\n"
    for i, user in enumerate(users):
        text += f"{i+1}. {user['_id']} - {user['referrals']} referrals\n"

    await message.reply(text)
