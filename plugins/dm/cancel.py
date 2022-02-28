# fileName : plugins/dm/cancel.py
# copyright ©️ 2021 nabilanavab




from pdf import PROCESS
from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as ILovePDF
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
#--------> CANCELS CURRENT PDF TO IMAGES WORK
#------------------->


@ILovePDF.on_message(filters.private & ~filters.edited & filters.command(["cancel"]))
async def cancelP2I(bot, message):
    try:
        if (message.chat.id in BANNED_USERS) or (
            (ADMIN_ONLY) and (message.chat.id not in ADMINS)
        ):
            await message.reply_text(
                UCantUse,
                reply_markup=button,
                quote=True
            )
            return
        PROCESS.remove(message.chat.id)
        await message.delete()          # delete /cancel if process canceled
    except Exception:
        try:
            await bot.send_chat_action(
                message.chat.id, "typing"
            )
            await message.reply_text(
                '🤔', quote=True
            )
        except Exception:
            pass


#                                                                                  Telegram: @nabilanavab
