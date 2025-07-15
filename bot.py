# bot.py

from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

Bot = Client(
    "ForceSubReferralBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="bot")
)
