# bot/start.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMINS
from database.mongo import db
from bot.force_sub import check_force_sub
from bot.media import deliver_media

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    user = message.from_user
    user_id = user.id
    args = message.text.split()

    # Register user
    await db.add_user(user_id)

    # Handle referral
    if len(args) > 1 and args[1].startswith("ref"):
        ref_id = args[1][3:]
        if ref_id.isdigit() and int(ref_id) != user_id:
            await db.add_referral(referrer_id=int(ref_id), referred_id=user_id)

    # Force Sub Check
    passed, markup = await check_force_sub(client, user_id)
    if not passed:
        return await message.reply(
            "🔒 <b>Join required channels to use this bot.</b>",
            reply_markup=markup,
            parse_mode="html"
        )

    # Deliver media if allowed
    delivered = await deliver_media(client, user_id, message.chat.id)
    if not delivered:
        if user_id in ADMINS:
            await message.reply(
                "✅ You're subscribed! Come back later for more media.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⚙️ Open Settings", callback_data="settings")]])
            )
        else:
            await message.reply("✅ You're subscribed! Come back later for more media.")

@Client.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):
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
    await message.reply_text(HELP_TEXT, parse_mode="html")
