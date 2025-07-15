# bot/help.py

from pyrogram import Client, filters
from pyrogram.types import Message

HELP_TEXT = (
    "<b>🛠 Bot Commands & Help</b>\n\n"
    "<b>/start</b> - Begin interaction with the bot\n"
    "<b>/help</b> - Show this help message\n"
    "<b>/refer</b> - Get your referral link\n"
    "<b>/bonus</b> - Claim your referral bonus\n"
    "<b>/settings</b> - Customize bot behavior (admin only)\n"
    "<b>/stats</b> - View bot usage stats (admin only)\n\n"
    "✅ To receive media, you must join the required channels.\n"
    "🎁 Share your referral link to earn bonus media."
)

@Client.on_message(filters.command("help") & filters.private)
async def help_handler(client: Client, message):
    await message.reply_text(HELP_TEXT, parse_mode="html")
