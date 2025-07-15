# bot/media.py

import random, asyncio
from pyromod import Client
from database.mongo import db

from config import COOLDOWN_HOURS, DELETE_DELAY

async def deliver_media(client: Client, user_id: int, chat_id: int):
    settings = await db.get_settings()

    # ⏳ Cooldown Check
    if not await db.can_access(user_id, COOLDOWN_HOURS):
        wait = await db.cooldown_remaining(user_id, COOLDOWN_HOURS)
        return await client.send_message(chat_id, f"⏳ Please wait {wait} before requesting more media.")

    # 🎞 Media Config
    from config import MEDIA_COUNT
    count = MEDIA_COUNT
    caption = settings.get("caption", "")
    buttons = await db.parse_buttons(settings.get("buttons", ""))
    media_pool = await db.get_media_pool()

    if not media_pool:
        return await client.send_message(chat_id, "⚠️ No media available yet. Please try again later.")

    # 🎲 Random Media Selection
    selected = random.sample(media_pool, min(len(media_pool), count))
    await db.set_last_access(user_id)

    media_channel = settings.get("media_channel")
    if not media_channel:
        return await client.send_message(chat_id, "⚠️ Media channel not set. Please contact an admin.")

    # 📤 Send Media One-by-One
    for msg_id in selected:
        try:
            sent = await client.copy_message(
                chat_id,
                media_channel,
                msg_id,
                caption=caption,
                reply_markup=buttons
            )
            if DELETE_DELAY > 0:
                asyncio.create_task(delete_after(client, sent.chat.id, sent.id, DELETE_DELAY * 60))
        except Exception as e:
            print(f"[ERROR] Failed to send media ID {msg_id}: {e}")
            continue
    return True

async def delete_after(client: Client, chat_id: int, message_id: int, delay: int):
    await asyncio.sleep(delay)
    try:
        await client.delete_messages(chat_id, message_id)
    except:
        pass
