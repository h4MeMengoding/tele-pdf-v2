# fileName : plugins/dm/id.py
# copyright ©️ 2021 nabilanavab




from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as ILovePDF
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

menuFitur = """Terimakasih sudah menggunakan InHame PDF Bot, berikut perintah yang tersedia 

`Umum`
/start - memulai bot
/id - melihat id telegram Anda
/feedback - memberikan saran kepada dev untuk bot
/menu - menampilkan menu perintah yang tersedia
/dev - informasi tentang developer(pengembang) bot ini
/report - melaporkan bug/error pada bot

`Image to PDF`
/buat - membuat file pdf
/hapus - menghapus antrian sebelumnya

`PDF to ...`
__To Image__
__To Text__
__Encrypt__ (memberi password pada pdf)
__Decrypt__ (menghapus password pada pdf)
__Compress__ (mengecilkan ukuran pdf)
__Rotate__ (mengubah rotasi gambar pdf)
__Split__ (memilih isi pdf untuk diambil per page)
__Merge__ 
__Stamp__ (memberi watermark pada pdf)
__Rename__ (merubah nama file pdf)
"""

#--------------->
#--------> GET USER ID (/id)
#------------------->


@ILovePDF.on_message(filters.private & ~filters.edited & filters.command(["menu"]))
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
            menuFitur, quote=True
        )
    except Exception:
        pass


#                                                                                  Telegram: @nabilanavab
