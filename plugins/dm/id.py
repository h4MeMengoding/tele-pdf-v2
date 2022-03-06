'''

█ █▄ █    █▄█ ▄▀▄ █▄ ▄█ ██▀    █▀▄ █▀▄ █▀ 
█ █ ▀█    █ █ █▀█ █ ▀ █ █▄▄    █▀  █▄▀ █▀ 
                        Dev : IlhamGUD

'''

from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as InHamePDF
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup




#--------------->
#--------> Config var.
#------------------->

BANNED_USERS=Config.BANNED_USERS
ADMIN_ONLY=Config.ADMIN_ONLY
ADMINS=Config.ADMINS

#--------------->
#--------> LOCAL VARIABLES
#------------------->

UCantUse = "Kamu telah di-BAN karena melanggar ketentuan"


button=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "CHAT DEV",
                    url="https://t.me/ilhamshff"
                )
            ]
       ]
    )

#--------------->
#--------> GET USER ID (/id)
#------------------->


@InHamePDF.on_message(filters.private & ~filters.edited & filters.command(["id"]))
async def userId(bot, message):
    try:
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        if (message.chat.id in BANNED_USERS) or (
            (ADMIN_ONLY) and (message.chat.id not in ADMINS)
        ):
            await message.reply_text(
                UCantUse,
                reply_markup=button
            )
            return
        await message.reply_text(
            f'ID Telegram anda: `{message.chat.id}`', quote=True
        )
    except Exception:
        pass


# Copyright InHame Dev
