# bot/callbacks.py

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMINS
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

        settings = await db.get_settings()
        media_channel = settings.get("media_channel")
        if not media_channel:
            return await cb.answer("⚠️ Media channel not set.", show_alert=True)

        msg_id = random.choice(media)
        caption = settings.get("caption", "")
        buttons = await db.parse_buttons(settings.get("buttons", ""))
        await client.copy_message(cb.message.chat.id, media_channel, msg_id, caption=caption, reply_markup=buttons, parse_mode="html")

    elif data == "resetmedia":
        await db.reset_media_pool()
        await cb.answer("✅ Media pool reset.", show_alert=True)

    # Handlers for settings
    elif data.startswith("set"):
        await cb.message.delete()
        setting = data.split("set")[1]

        if setting == "media":
            msg = await client.ask(cb.message.chat.id, "Forward media to me to set the media pool.")
            if msg.media:
                await db.add_media(msg.id)
                await msg.reply("✅ Media added to pool.")
        elif setting == "caption":
            msg = await client.ask(cb.message.chat.id, "Send me the new caption.")
            await db.set_setting("caption", msg.text)
            await msg.reply("✅ Caption has been set.")
        elif setting == "buttons":
            msg = await client.ask(cb.message.chat.id, "Send me the new buttons in the correct format.")
            await db.set_setting("buttons", msg.text)
            await msg.reply("✅ Buttons saved.")
        elif setting == "infobutton":
            msg = await client.ask(cb.message.chat.id, "Send me the new info button in the correct format.")
            await db.set_setting("infobutton", msg.text)
            await msg.reply("✅ Info button set.")
        elif setting == "delay":
            msg = await client.ask(cb.message.chat.id, "Send me the new delay in minutes.")
            if msg.text.isdigit():
                await db.set_setting("delete_delay", int(msg.text))
                await msg.reply(f"✅ Auto-delete delay set to {msg.text} minutes")
        elif setting == "cooldown":
            msg = await client.ask(cb.message.chat.id, "Send me the new cooldown in hours.")
            if msg.text.isdigit():
                await db.set_setting("cooldown_hours", int(msg.text))
                await msg.reply(f"✅ Cooldown time set to {msg.text} hours")
        elif setting == "refreward":
            msg = await client.ask(cb.message.chat.id, "Send me the new referral reward.")
            if msg.text.isdigit():
                await db.set_setting("ref_bonus", int(msg.text))
                await msg.reply(f"✅ Referral reward set to {msg.text} media per user")
        elif setting == "refcap":
            msg = await client.ask(cb.message.chat.id, "Send me the new referral cap.")
            if msg.text.isdigit():
                await db.set_setting("ref_cap", int(msg.text))
                await msg.reply(f"✅ Referral cap set to {msg.text} media")
        elif setting == "mediachannel":
            msg = await client.ask(cb.message.chat.id, "Forward a message from the media channel.")
            if msg.forward_from_chat:
                await db.set_setting("media_channel", msg.forward_from_chat.id)
                await msg.reply("✅ Media channel has been set.")

    elif data == "managefs":
        channels = await db.get_force_sub_channels()
        text = "<b>📢 Manage Force-Sub Channels</b>\n\n"
        if not channels:
            text += "No channels added yet."
        else:
            for i, channel in enumerate(channels):
                text += f"{i+1}. `{channel}`\n"

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Channel", callback_data="addfs")],
            [InlineKeyboardButton("➖ Remove Channel", callback_data="remfs")],
            [InlineKeyboardButton("🔙 Back", callback_data="settings")]
        ])
        await cb.message.edit(text, reply_markup=buttons)

    elif data == "addfs":
        msg = await client.ask(cb.message.chat.id, "Forward a message from the channel to add.")
        if msg.forward_from_chat:
            await db.add_force_sub_channel(msg.forward_from_chat.id)
            await msg.reply("✅ Channel added.")

    elif data == "remfs":
        msg = await client.ask(cb.message.chat.id, "Send me the channel ID to remove.")
        if msg.text.isdigit():
            await db.remove_force_sub_channel(int(msg.text))
            await msg.reply("✅ Channel removed.")
