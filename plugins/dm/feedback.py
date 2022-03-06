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
#--------> config vars
#------------------->

BANNED_USERS=Config.BANNED_USERS
ADMIN_ONLY=Config.ADMIN_ONLY
ADMINS=Config.ADMINS

#--------------->
#--------> LOCAL VARIABLES
#------------------->

UCantUse = "Kamu telah di-BAN karena melanggar ketentuan"


feedbackMsg = """
[Tulis feedback 📋](https://tellonym.me/Developer_InHame)
"""


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
#--------> REPLY TO /feedback
#------------------->


@InHamePDF.on_message(filters.private & filters.command(["feedback"]) & ~filters.edited)
async def feedback(bot, message):
    try:
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        if (message.chat.id in BANNED_USERS) or (
            (ADMIN_ONLY) and (message.chat.id not in ADMINS)
        ):
            await message.reply_text(
                UCantUse,
                reply_markup=button,
                quote=True
            )
            return
        await bot.send_message(
            message.chat.id, feedbackMsg,
            disable_web_page_preview = True
        )
    except Exception:
        pass


# Copyright InHame Dev
