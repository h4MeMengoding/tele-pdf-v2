'''

█ █▄ █    █▄█ ▄▀▄ █▄ ▄█ ██▀    █▀▄ █▀▄ █▀ 
█ █ ▀█    █ █ █▀█ █ ▀ █ █▄▄    █▀  █▄▀ █▀ 
                        Dev : IlhamGUD

'''

from pyrogram.types import Message
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup




#--------------->
#--------> LOCAL VARIABLES
#------------------->

pdfInfoMsg = """`Apa yang ingin saya lakukan dengan file ini?`

Nama FIle : `{}`
Ukuran File : `{}`

`Jumlah Halaman: {}`"""

#--------------->
#--------> EDIT CHECKPDF MESSAGE (IF PDF & NOT ENCRYPTED)
#------------------->

# convert tidak diketahui to known page number msgs
async def toKnown(callbackQuery, number_of_pages):
    try:
        fileName = callbackQuery.message.reply_to_message.document.file_name
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        
        await callbackQuery.edit_message_text(
            pdfInfoMsg.format(
                fileName, await gSF(fileSize), number_of_pages
            ),
            reply_markup = InlineKeyboardMarkup(
                [
            [
                InlineKeyboardButton(
                    "INFORMASI PDF",
                    callback_data="pdfInfo"
                )
            ],
            [
                InlineKeyboardButton(
                    "TO IMAGE 🖼️",
                    callback_data="toImage"
                ),
                InlineKeyboardButton(
                    "TO TEXT ✏️",
                    callback_data="toText"
                )
            ],
            [
                InlineKeyboardButton(
                    "ENCRYPT 🔐",
                    callback_data="encrypt"
                ),
                InlineKeyboardButton(
                    "DECRYPT 🔓",
                    callback_data="decrypt"
                )
            ],
            [
                InlineKeyboardButton(
                    "COMPRESS 🗜️",
                    callback_data="compress"
                ),
                InlineKeyboardButton(
                    "ROTATE 🤸",
                    callback_data="rotate"
                )
            ],
            [
                InlineKeyboardButton(
                    "SPLIT ✂️",
                    callback_data="split"
                ),
                InlineKeyboardButton(
                    "MERGE 🧬",
                    callback_data="merge"
                )
            ],
            [
                InlineKeyboardButton(
                    "STAMP ™️",
                    callback_data="stamp"
                ),
                InlineKeyboardButton(
                    "RENAME ✏️",
                    callback_data="rename"
                )
            ]
        ]
            )
        )
    except Exception as e:
        print(f"plugins/toKnown: {e}")


# Copyright InHame Dev
