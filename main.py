# main.py

import asyncio
from pyrogram import idle
from bot import Bot
from database.mongo import db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def send_referral_reminders():
    users = await db.get_all_users()
    bot_username = (await Bot.get_me()).username

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
        except:
            continue

async def main():
    await Bot.start()
    await db.connect()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_referral_reminders, "interval", hours=8)
    scheduler.start()

    print("Bot is running...")
    await idle()
    await Bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
