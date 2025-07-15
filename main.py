# main.py

import asyncio
from pyrogram import Client, idle
from database.mongo import db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN

Bot = None

async def send_referral_reminders():
    if Bot is None:
        return
    users = await db.get_all_users()
    try:
        bot_username = (await Bot.get_me()).username
    except Exception as e:
        print(f"Error getting bot username: {e}")
        return

    for user in users:
        user_id = user["_id"]
        count = await db.get_referral_count(user_id)
        bonus = await db.get_available_bonus(user_id)

        referral_link = f"https://t.me/{bot_username}?start=ref{user_id}"
        share_text = "🎬 Get free media by using this bot! 👇"
        share_url = f"https://t.me/share/url?url={referral_link}&text={share_text}"

        text = (
            "🚀 <b>Earn bonus media by inviting friends!</b>\n\n"
            f"🔗 <b>Your Referral Link:</b>\n{referral_link}\n\n"
            f"🎯 Referrals: {count}\n"
            f"🎁 Bonus Available: {bonus} media"
        )

        button = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Share Now", url=share_url)]
        ])

        try:
            await Bot.send_message(user_id, text, reply_markup=button, parse_mode="html")
        except Exception as e:
            print(f"Failed to send reminder to {user_id}: {e}")
            continue

async def main():
    global Bot
    await db.connect()

    if API_ID and API_HASH and BOT_TOKEN:
        Bot = Client(
            "ForceSubReferralBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="bot")
        )

        scheduler = AsyncIOScheduler()
        scheduler.add_job(send_referral_reminders, "interval", hours=8)
        scheduler.start()

        print("Bot is running...")
        async with Bot:
            await idle()
    else:
        print("Bot token, API ID, or API hash is not configured. Exiting.")


if __name__ == "__main__":
    asyncio.run(main())
