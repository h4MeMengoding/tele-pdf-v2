# fileName : Plugins/dm/photo.py
# copyright ©️ 2021 nabilanavab




import os
from pdf import PDF
from PIL import Image
from pdf import invite_link
from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from time import sleep




#--------------->
#--------> Config var.
#------------------->

UPDATE_CHANNEL=Config.UPDATE_CHANNEL
BANNED_USERS=Config.BANNED_USERS
ADMIN_ONLY=Config.ADMIN_ONLY
ADMINS=Config.ADMINS

#--------------->
#--------> LOCAL VARIABLES
#------------------->

UCantUse = "Kamu telah di-BAN karena melanggar ketentuan"


imageAdded = """`✅ - Berhasil Menambahkan {} halaman ke pdf`
"""


forceSubMsg = """Tunggu [{}](tg://user?id={})..!!

Karena alasan traffic server maka hanya Anggota channel yang Dapat Menggunakan
    
Anda diwajibkan untuk bergabung kedalam channel.

Klik "refresh" jika sudah bergabung.. 
"""

gmbrAlrt = """`*⏱️pesan akan terhapus dalam 8s
    Note : Jika ingin menambahkan foto lainnya dalam satu pdf silahkan kirim foto sebelum melakukan /buat`

/buat [Nama Filemu Bebas] - untuk membuat nama pdf
/hapus - untuk menghapus semua halaman
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
#--------> REPLY TO IMAGES
#------------------->


@ILovePDF.on_message(filters.private & ~filters.edited & filters.photo)
async def images(bot, message):
    try:
        global invite_link
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        # CHECK USER IN CHANNEL (IF UPDATE_CHANNEL ADDED)
        if UPDATE_CHANNEL:
            try:
                await bot.get_chat_member(
                    str(UPDATE_CHANNEL), message.chat.id
                )
            except Exception:
                if invite_link == None:
                    invite_link=await bot.create_chat_invite_link(
                        int(UPDATE_CHANNEL)
                    )
                await bot.send_message(
                    message.chat.id,
                    forceSubMsg.format(
                        message.from_user.first_name, message.chat.id
                    ),
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "BERGABUNG",
                                    url=invite_link.invite_link
                                ),
                                InlineKeyboardButton(
                                    "REFRESH",
                                    callback_data="refresh"
                                )
                            ]
                        ]
                    )
                )
                return
        # CHECKS IF USER BAN/ADMIN..
        if (message.chat.id in BANNED_USERS) or (
            (ADMIN_ONLY) and (message.chat.id not in ADMINS)
        ):
            await message.reply_text(
                UCantUse,
                reply_markup=button
            )
            return
        imageReply = await bot.send_message(
            message.chat.id,
            "`⏳ - Mengunduh Gambar Anda`",
            reply_to_message_id = message.message_id
        )
        if not isinstance(PDF.get(message.chat.id), list):
            PDF[message.chat.id] = []
        await message.download(
            f"{message.chat.id}/{message.chat.id}.jpg"
        )
        img = Image.open(
            f"{message.chat.id}/{message.chat.id}.jpg"
        ).convert("RGB")
        PDF[message.chat.id].append(img)
        await imageReply.edit(
            imageAdded.format(len(PDF[message.chat.id]))
        )
        alrtMsg = await bot.send_message(
            message.chat.id, gmbrAlrt #untuk mengirim pesan peringatan
        )
        sleep(8)
        await bot.delete_messages(
            chat_id = message.chat.id,
            message_ids = alrtMsg.message_id
        )
    except Exception:
        pass


#                                                                                  Telegram: @nabilanavab
