# bot/force_sub.py

from pyromod import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.mongo import db

async def check_force_sub(client: Client, user_id: int):
    required_channels = await db.get_force_sub_channels()
    strict_mode = (await db.get_settings()).get("strict_mode", False)

    missing = []
    for ch_id in required_channels:
        try:
            member = await client.get_chat_member(ch_id, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                missing.append(ch_id)
        except:
            missing.append(ch_id)

    if not missing:
        return True, None

    # If strict mode, block access
    if strict_mode:
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton("✅ I’ve Rejoined", callback_data="recheck")]]
        )
        return False, buttons

    # List channels to join
    buttons = []
    for ch_id in missing:
        try:
            chat = await client.get_chat(ch_id)
            title = chat.title
            link = chat.invite_link or await client.export_chat_invite_link(ch_id)
            buttons.append([InlineKeyboardButton(f"📢 Join {title}", url=link)])
        except:
            continue
    buttons.append([InlineKeyboardButton("✅ I’ve Joined", callback_data="recheck")])

    return False, InlineKeyboardMarkup(buttons)
