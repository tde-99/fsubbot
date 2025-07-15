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
        "/topref - Show top referrers\n\n"
        "<b>Settings Help</b>\n\n"
        "Here is a detailed explanation of each setting:\n\n"
        "<b>Set Media Channel</b>: This is the channel where you will store all the media that the bot will send to users. Forward a message from this channel to the bot to set it.\n\n"
        "<b>Set Media Count</b>: This is the number of media that will be sent to a user each time they use the bot.\n\n"
        "<b>Set Caption</b>: This is the caption that will be sent with each media.\n\n"
        "<b>Set Buttons</b>: These are the inline buttons that will be sent with each media. You can use them to add links to your website or other social media.\n\n"
        "<b>Set Info Button</b>: This is an optional button that will be shown below the final warning message when a user has not joined the required channels.\n\n"
        "<b>Set Auto-Delete</b>: This is the time in minutes after which the media sent by the bot will be deleted.\n\n"
        "<b>Set Cooldown</b>: This is the time in hours that a user has to wait before they can use the bot again.\n\n"
        "<b>Set Referral Reward</b>: This is the number of media that a user will receive for each successful referral.\n\n"
        "<b>Set Referral Cap</b>: This is the maximum number of bonus media that a user can receive from referrals.\n\n"
        "<b>Toggle Strict Mode</b>: If this is enabled, users will be completely blocked from using the bot until they join all the required channels.\n\n"
        "<b>Manage Force-Sub Channels</b>: This is where you can add or remove the channels that users must join to use the bot.\n\n"
        "<b>View Stats</b>: This will show you the total number of users and media in the bot.\n\n"
        "<b>Preview Media</b>: This will send you a random media from the media pool so you can see what it looks like.\n\n"
        "<b>Reset Media</b>: This will clear all the saved media from the bot.\n\n"
        "<b>Close</b>: This will close the settings panel."
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
