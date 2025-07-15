# bot/settings_panel.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from config import ADMINS
from database.mongo import db

@Client.on_message(filters.command("settings") & filters.user(ADMINS))
async def open_settings_panel(client: Client, message: Message):
    settings = await db.get_settings()

    rows = [
        [InlineKeyboardButton("📢 Set Media Channel", callback_data="setmediachannel")],
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

    text = (
        "<b>⚙️ Admin Settings Panel</b>\n\n"
        "Here are your configuration options:\n\n"
        "📦 <b>Set Media Count</b> — Number of media sent per user\n"
        "💬 <b>Set Caption</b> — Caption shown with each media\n"
        "🔘 <b>Set Buttons</b> — Inline buttons under media (custom links)\n"
        "ℹ️ <b>Set Info Button</b> — Optional button below info messages\n"
        "🕒 <b>Set Auto-Delete</b> — Auto-delete media after X minutes\n"
        "⏳ <b>Set Cooldown</b> — Time users must wait before next access\n"
        "🎁 <b>Set Referral Reward</b> — How many media per referral\n"
        "🚫 <b>Set Referral Cap</b> — Max bonus media from referrals\n"
        "🛑 <b>Toggle Strict Mode</b> — Fully block users until they join\n"
        "👥 <b>Manage Force-Sub Channels</b> — Add/remove required channels\n"
        "📊 <b>View Stats</b> — See total users, media, and referrals\n"
        "🧪 <b>Preview Media</b> — Preview media from saved pool\n"
        "♻️ <b>Reset Media</b> — Clear all saved media and captions\n"
        "🔙 <b>Close</b> — Exit this panel\n"
    )

    await message.reply(text, reply_markup=InlineKeyboardMarkup(rows), parse_mode=ParseMode.HTML)
