from pyrogram import Client, filters
from utils import temp
from pyrogram.types import Message
from database.users_chats_db import db
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import SUPPORT_CHAT

async def banned_users(_, client, message: Message):
    return (
        message.from_user is not None or not message.sender_chat
    ) and message.from_user.id in temp.BANNED_USERS

banned_user = filters.create(banned_users)

async def disabled_chat(_, client, message: Message):
    return message.chat.id in temp.BANNED_CHATS

disabled_group=filters.create(disabled_chat)


@Client.on_message(filters.private & banned_user & filters.incoming)
async def ban_reply(bot, message):
    ban = await db.get_ban_status(message.from_user.id)
    await message.reply(f'sᴏʀʀʏ ᴅᴜᴅᴇ, ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ.. \nBan Reason: {ban["ban_reason"]}')

@Client.on_message(filters.group & disabled_group & filters.incoming)
async def grp_bd(bot, message):
    buttons = [[
        InlineKeyboardButton('᯽sᴜᴘᴘᴏʀᴛ᯽', url=f'https://t.me/{SUPPORT_CHAT}')
    ]]
    reply_markup=InlineKeyboardMarkup(buttons)
    vazha = await db.get_chat(message.chat.id)
    k = await message.reply(
        text=f"ᴄʜᴀᴛ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ 🐞\n\nᴍʏ ᴀᴅᴍɪɴs ʜᴀs ʀᴇsᴛʀɪᴄᴛᴇᴅ ᴍᴇ ғᴏʀ ᴡᴏʀᴋɪɴɢ ʜᴇʀᴇ! ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜɴʙᴀɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄᴏɴᴛᴀᴄᴛ ᴏɴ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ\nReason : <code>{vazha['reason']}</code>.",
        reply_markup=reply_markup)
    try:
        await k.pin()
    except:
        pass
    await bot.leave_chat(message.chat.id)
