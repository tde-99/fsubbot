# config.py

import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

MONGO_URI = os.getenv("MONGO_URI")
ADMINS = list(map(int, os.getenv("ADMINS", "").split()))

MEDIA_CHANNEL = int(os.getenv("MEDIA_CHANNEL"))
MEDIA_COUNT = int(os.getenv("MEDIA_COUNT", "1"))
DELETE_DELAY = int(os.getenv("DELETE_DELAY", "0"))
COOLDOWN_HOURS = int(os.getenv("COOLDOWN_HOURS", "0"))
REFERRAL_REWARD = int(os.getenv("REFERRAL_REWARD", "1"))
REFERRAL_CAP = int(os.getenv("REFERRAL_CAP", "0"))
