# bot/callbacks.py

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMINS, MEDIA_CHANNEL
from database.mongo import db
from bot.force_sub import check_force_sub
import random

@Client.on_callback_query(filters.regex("recheck"))
async def recheck_force_sub(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    passed, markup = await check_force_sub(client, user_id)

    if passed:
        await callback_query.message.edit("✅ You have joined all required channels. Please use /start again.")
    else:
        await callback_query.answer("❌ You must join the channels first.", show_alert=True)

# Admin Settings Panel Button Handlers

@Client.on_callback_query(filters.user(ADMINS))
async def admin_callbacks(client: Client, cb: CallbackQuery):
    data = cb.data

    if data == "close":
        return await cb.message.delete()

    if data == "togglestrict":
        settings = await db.get_settings()
        current = settings.get("strict_mode", False)
        await db.set_setting("strict_mode", not current)
        await cb.answer(f"{'Enabled' if not current else 'Disabled'} strict mode ✅", show_alert=True)

    elif data == "dostats":
        users = await db.get_all_users()
        media = await db.get_media_pool()
        msg = (
            f"👥 Total Users: {len(users)}\n"
            f"📦 Media Count: {len(media)}\n"
        )
        await cb.message.edit(msg, reply_markup=cb.message.reply_markup)

    elif data == "dopreview":
        media = await db.get_media_pool()
        if not media:
            return await cb.answer("⚠️ No media in pool.", show_alert=True)
        msg_id = random.choice(media)
        caption = (await db.get_settings()).get("caption", "")
        buttons = await db.parse_buttons((await db.get_settings()).get("buttons", ""))
        await client.copy_message(cb.message.chat.id, MEDIA_CHANNEL, msg_id, caption=caption, reply_markup=buttons, parse_mode="html")

    elif data == "resetmedia":
        await db.reset_media_pool()
        await cb.answer("✅ Media pool reset.", show_alert=True)
