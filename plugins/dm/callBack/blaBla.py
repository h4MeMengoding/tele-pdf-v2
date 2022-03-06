# fileName : plugins/dm/callBack/blaBla.py
# copyright ©️ 2021 InHame Dev




from pdf import PROCESS
from pyrogram import filters
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup




#--------------->
#--------> LOCAL VARIABLES
#------------------->

error = filters.create(lambda _, __, query: query.data == "error")
closeme = filters.create(lambda _, __, query: query.data == "closeme")
underDev = filters.create(lambda _, __, query: query.data == "underDev")
notEncrypted = filters.create(lambda _, __, query: query.data == "notEncrypted")


@ILovePDF.on_callback_query(underDev)
async def _underDev(bot, callbackQuery):
    try:
        await callbackQuery.answer(
            "❗ - This feature is Under Development"
        )
    except Exception:
        pass


@ILovePDF.on_callback_query(error)
async def _error(bot, callbackQuery):
    try:
        await callbackQuery.answer(
            "Error---"
        )
    except Exception:
        pass


@ILovePDF.on_callback_query(closeme)
async def _closeme(bot, callbackQuery):
    try:
        try:
            await callbackQuery.message.delete()
        except Exception:
            pass
        await callbackQuery.answer(
            "`☑️ - Proses dibatalkan`"
        )
        PROCESS.remove(callbackQuery.message.chat.id)
    except Exception:
        pass


@ILovePDF.on_callback_query(notEncrypted)
async def _notEncrypted(bot, callbackQuery):
    try:
        await callbackQuery.answer(
            "❗ - FIle tidak diEncrypted"
        )
    except Exception:
        pass
