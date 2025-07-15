# bot/callbacks.py

from pyromod import Client
from pyrogram import filters
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
        await client.copy_message(cb.message.chat.id, media_channel, msg_id, caption=caption, reply_markup=buttons)

    elif data == "resetmedia":
        await db.reset_media_pool()
        await cb.answer("✅ Media pool reset.", show_alert=True)

    # Handlers for settings
    elif data.startswith("set"):
        await cb.message.delete()
        setting = data.split("set")[1]

        if setting == "caption":
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

    elif data == "help":
        await cb.message.edit(
            "<b>Settings Help</b>\n\n"
            "Here is a detailed explanation of each setting:\n\n"
            "<b>Set Media Channel</b>: This is the channel where you will store all the media that the bot will send to users. Forward a message from this channel to the bot to set it.\n\n"
            "<b>Set Media Count</b>: This is the number of media that will be sent to a user each time they use the bot.\n\n"
            "<b>Set Caption</b>: This is the caption that will be sent with each media.\n\n"
            "<b>Set Buttons</b>: These are the inline buttons that will be sent with each media. You can use them to add links to your website or other social media.\n\n"
            "<b>Set Info Button</b>: This is an optional button that will be shown below the final warning message when a user has not joined the required channels.\n\n"
            "<b>Set Auto-Delete</b>: This is the time in minutes after which the media sent by the bot will be deleted.\n\n"
            "<b>Set Cooldown</b>: This is the time in hours that a user has to wait before they can use the bot again.\n\n"
            "<b>Set Referral Reward</b>: This is the number of media that a user will receive for each successful referral.\n\n"
            "<b>Set Referral Cap</b>: This is the maximum number of bonus media that a user can receive from referrals.\n\n"
            "<b>Toggle Strict Mode</b>: If this is enabled, users will be completely blocked from using the bot until they join all the required channels.\n\n"
            "<b>Manage Force-Sub Channels</b>: This is where you can add or remove the channels that users must join to use the bot.\n\n"
            "<b>View Stats</b>: This will show you the total number of users and media in the bot.\n\n"
            "<b>Preview Media</b>: This will send you a random media from the media pool so you can see what it looks like.\n\n"
            "<b>Reset Media</b>: This will clear all the saved media from the bot.\n\n"
            "<b>Close</b>: This will close the settings panel.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="settings")]])
        )
