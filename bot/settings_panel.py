# bot/settings_panel.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMINS
from database.mongo import db

@Client.on_message(filters.command("settings") & filters.user(ADMINS))
async def open_settings_panel(client: Client, message: Message):
    settings = await db.get_settings()
    rows = [
        [InlineKeyboardButton("📦 Set Media Count", callback_data="setmedia")],
        [InlineKeyboardButton("💬 Set Caption", callback_data="setcaption")],
        [InlineKeyboardButton("🔘 Set Buttons", callback_data="setbuttons")],
        [InlineKeyboardButton("ℹ️ Set Info Button", callback_data="setinfobutton")],
        [InlineKeyboardButton("🕒 Set Auto-Delete", callback_data="setdelay")],
        [InlineKeyboardButton("⏳ Set Cooldown (hrs)", callback_data="setcooldown")],
        [InlineKeyboardButton("🎁 Set Referral Reward", callback_data="setrefreward")],
        [InlineKeyboardButton("🚫 Set Referral Cap", callback_data="setrefcap")],
        [InlineKeyboardButton("🛑 Toggle Strict Mode", callback_data="togglestrict")],
        [InlineKeyboardButton("👥 Manage Force-Sub Channels", callback_data="managefs")],
        [InlineKeyboardButton("📊 View Stats", callback_data="dostats")],
        [InlineKeyboardButton("🧪 Preview Media", callback_data="dopreview")],
        [InlineKeyboardButton("♻️ Reset Media", callback_data="resetmedia")],
        [InlineKeyboardButton("🔙 Close", callback_data="close")]
    ]

    await message.reply(
        "<b>⚙️ Admin Settings Panel</b>\nChoose an option below:",
        reply_markup=InlineKeyboardMarkup(rows),
        parse_mode="html"
    )
