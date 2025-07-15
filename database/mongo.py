# database/mongo.py

import motor.motor_asyncio
from config import MONGO_URI, MEDIA_CHANNEL
from datetime import datetime, timedelta
from bson.objectid import ObjectId

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
        self.db = self.client["force_sub_bot"]

    async def add_user(self, user_id: int):
        await self.db.users.update_one({"_id": user_id}, {"$setOnInsert": {"joined": datetime.utcnow()}}, upsert=True)

    async def get_all_users(self):
        return await self.db.users.find().to_list(length=None)

    async def set_setting(self, key: str, value):
        await self.db.settings.update_one({"_id": "main"}, {"$set": {key: value}}, upsert=True)

    async def get_settings(self):
        result = await self.db.settings.find_one({"_id": "main"}) or {}
        return result

    async def get_force_sub_channels(self):
        rows = await self.db.force_sub.find().to_list(length=None)
        return [row["_id"] for row in rows]

    async def add_force_sub_channel(self, chat_id: int):
        await self.db.force_sub.update_one({"_id": chat_id}, {"$set": {}}, upsert=True)

    async def remove_force_sub_channel(self, chat_id: int):
        await self.db.force_sub.delete_one({"_id": chat_id})

    async def get_media_pool(self):
        docs = await self.db.media.find().to_list(length=None)
        return [doc["msg_id"] for doc in docs]

    async def add_media(self, msg_id: int):
        await self.db.media.update_one({"msg_id": msg_id}, {"$set": {}}, upsert=True)

    async def reset_media_pool(self):
        await self.db.media.delete_many({})

    async def can_access(self, user_id: int, cooldown: int):
        user = await self.db.users.find_one({"_id": user_id})
        last = user.get("last_access")
        if not last: return True
        return datetime.utcnow() - last >= timedelta(hours=cooldown)

    async def set_last_access(self, user_id: int):
        await self.db.users.update_one({"_id": user_id}, {"$set": {"last_access": datetime.utcnow()}})

    async def cooldown_remaining(self, user_id: int, cooldown: int):
        user = await self.db.users.find_one({"_id": user_id})
        last = user.get("last_access", datetime.utcnow())
        delta = timedelta(hours=cooldown) - (datetime.utcnow() - last)
        mins = max(int(delta.total_seconds() / 60), 0)
        return f"{mins} minutes"

    async def add_referral(self, referrer_id: int, referred_id: int):
        already = await self.db.users.find_one({"_id": referred_id})
        if already.get("referred"): return
        await self.db.users.update_one({"_id": referred_id}, {"$set": {"referred": referrer_id}})
        await self.db.users.update_one({"_id": referrer_id}, {"$inc": {"referrals": 1}})

    async def get_referral_count(self, user_id: int):
        user = await self.db.users.find_one({"_id": user_id}) or {}
        return user.get("referrals", 0)

from config import REFERRAL_CAP, REFERRAL_REWARD

async def get_available_bonus(self, user_id: int):
    total_refs = await self.get_referral_count(user_id)
    used = (await self.db.users.find_one({"_id": user_id}) or {}).get("bonus_used", 0)
    available = min(REFERRAL_CAP, total_refs * REFERRAL_REWARD) - used
    return max(available, 0)

    async def use_bonus_media(self, user_id: int):
        available = await self.get_available_bonus(user_id)
        if available <= 0: return []

        pool = await self.get_media_pool()
        if not pool: return []

        from random import sample
        selected = sample(pool, min(len(pool), int(available)))
        await self.db.users.update_one({"_id": user_id}, {"$inc": {"bonus_used": len(selected)}})
        return selected

    async def parse_buttons(self, text: str):
        if not text: return None
        from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        rows = []
        for line in text.split("\n"):
            row = []
            for btn in line.strip().split("|"):
                if "=" in btn:
                    label, url = btn.split("=", 1)
                    row.append(InlineKeyboardButton(label.strip(), url=url.strip()))
            if row: rows.append(row)
        return InlineKeyboardMarkup(rows)

db = MongoDB()
