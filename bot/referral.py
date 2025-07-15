# bot/referral.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.mongo import db
import asyncio

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
    settings = await db.get_settings()
    media_channel = settings.get("media_channel")

    if not media_channel:
        return await message.reply("⚠️ Media channel not set. Please contact an admin.")

    bonus_media_ids = await db.use_bonus_media(user_id)

    if not bonus_media_ids:
        return await message.reply("🎁 You have no bonus media to claim.")

    await message.reply(f"🎉 You have claimed {len(bonus_media_ids)} bonus media! They will be sent shortly.")

    for msg_id in bonus_media_ids:
        caption = settings.get("caption", "")
        buttons = await db.parse_buttons(settings.get("buttons", ""))
        delete_delay = settings.get("delete_delay", 0)

        try:
            sent = await client.copy_message(
                chat_id=user_id,
                from_chat_id=media_channel,
                message_id=msg_id,
                caption=caption,
                parse_mode="html",
                reply_markup=buttons
            )
            if delete_delay > 0:
                asyncio.create_task(delete_after(client, sent.chat.id, sent.id, delete_delay * 60))
        except Exception as e:
            print(f"[ERROR] Failed to send bonus media ID {msg_id}: {e}")
            continue

async def delete_after(client: Client, chat_id: int, message_id: int, delay: int):
    await asyncio.sleep(delay)
    try:
        await client.delete_messages(chat_id, message_id)
    except:
        pass
