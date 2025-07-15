# bot/referral.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.mongo import db

@Client.on_message(filters.command("refer") & filters.private)
async def refer_command(client: Client, message: Message):
    user_id = message.from_user.id
    bot_username = (await client.get_me()).username

    referral_link = f"https://t.me/{bot_username}?start=ref{user_id}"
    count = await db.get_referral_count(user_id)
    bonus = await db.get_available_bonus(user_id)

    share_url = f"https://t.me/share/url?url={referral_link}&text=🎬 Get free media from this Telegram bot!"

    reply_text = (
        "<b>🎁 Referral Program</b>\n\n"
        f"🔗 Your referral link:\n{referral_link}\n\n"
        f"👥 Total Referrals: {count}\n"
        f"🎁 Bonus Media Available: {bonus}"
    )

    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Share Now", url=share_url)]
    ])
    await message.reply(reply_text, reply_markup=button, parse_mode="html")


@Client.on_message(filters.command("bonus") & filters.private)
async def claim_bonus(client: Client, message: Message):
    user_id = message.from_user.id
    caption = (await db.get_settings()).get("caption", "")
    buttons = await db.parse_buttons((await db.get_settings()).get("buttons", ""))

    bonus_msgs = await db.use_bonus_media(user_id)
    if not bonus_msgs:
        return await message.reply("❌ No bonus media available. Invite others to earn bonus.")

    for msg_id in bonus_msgs:
        try:
            sent = await client.copy_message(
                message.chat.id,
                from_chat_id=(await db.get_settings()).get("media_channel", -100),
                message_id=msg_id,
                caption=caption,
                parse_mode="html",
                reply_markup=buttons
            )
            delay = (await db.get_settings()).get("delete_delay", 0)
            if delay:
                await asyncio.sleep(delay * 60)
                await client.delete_messages(sent.chat.id, sent.id)
        except:
            continue
