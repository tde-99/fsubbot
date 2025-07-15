# config.py

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram API credentials
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# MongoDB connection URI
MONGO_URI = os.getenv("MONGO_URI")

# List of admin user IDs
ADMINS = list(map(int, os.getenv("ADMINS", "").split()))

# ID of the channel where media is stored
MEDIA_CHANNEL = int(os.getenv("MEDIA_CHANNEL"))

# Number of media to send per user
MEDIA_COUNT = int(os.getenv("MEDIA_COUNT", "1"))

# Delay in minutes after which media is deleted
DELETE_DELAY = int(os.getenv("DELETE_DELAY", "0"))

# Cooldown in hours between user accesses
COOLDOWN_HOURS = int(os.getenv("COOLDOWN_HOURS", "0"))

# Number of media to give as a reward for a successful referral
REFERRAL_REWARD = int(os.getenv("REFERRAL_REWARD", "1"))

# Maximum number of bonus media a user can get from referrals
REFERRAL_CAP = int(os.getenv("REFERRAL_CAP", "0"))
