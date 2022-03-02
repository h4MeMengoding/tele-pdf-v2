# fileName : plugins/dm/Callback/pdfMetaData.py
# copyright ©️ 2021 nabilanavab




import fitz
import time
import shutil
from pdf import PROCESS
from pyrogram import filters
from plugins.progress import progress
from pyrogram import Client as ILovePDF
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup




#--------------->
#--------> LOCAL VARIABLES
#------------------->

pdfInfoMsg = """`Apa yang ingin saya lakukan dengan file ini?`

Nama FIle: `{}`
Ukuran File: `{}`

`Jumlah Halaman: {}`"""

encryptedMsg = """`FILE IS ENCRYPTED` 🔐

Nama FIle: `{}`
Ukuran File: `{}`

`Jumlah Halaman: {}`"""

#--------------->
#--------> PDF META DATA
#------------------->

pdfInfo = filters.create(lambda _, __, query: query.data == "pdfInfo")
KpdfInfo = filters.create(lambda _, __, query: query.data.startswith("KpdfInfo"))


@ILovePDF.on_callback_query(pdfInfo)
async def _pdfInfo(bot, callbackQuery):
    try:
        # CHECKS PROCESS
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "⏳ - Sedang dalam proses"
            )
            return
        # CB MESSAGE DELETES IF USER DELETED PDF
        try:
            fileExist = callbackQuery.message.reply_to_message.document.file_id
        except Exception:
            await bot.delete_messages(
                chat_id = callbackQuery.message.chat.id,
                message_ids = callbackQuery.message.message_id
            )
            return
        # ADD TO PROCESS
        PROCESS.append(callbackQuery.message.chat.id)
        # DOWNLOADING STARTED
        downloadMessage = await callbackQuery.edit_message_text(
            "`📥 - Mendownload PDF`",
        )
        pdf_path = f"{callbackQuery.message.message_id}/pdfInfo.pdf"
        file_id = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        # DOWNLOAD PROGRESS
        c_time = time.time()
        downloadLoc = await bot.download_media(
            message = file_id,
            file_name = pdf_path,
            progress = progress,
            progress_args = (
                fileSize,
                downloadMessage,
                c_time
            )
        )
        # CHECKS IS DOWNLOADING COMPLETED OR PROCESS CANCELED
        if downloadLoc is None:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        # OPEN FILE WITH FITZ
        with fitz.open(pdf_path) as pdf:
            isPdf = pdf.is_pdf
            metaData = pdf.metadata
            isEncrypted = pdf.is_encrypted
            number_of_pages = pdf.pageCount
            # CHECKS IF FILE ENCRYPTED
            if isPdf and isEncrypted:
                pdfMetaData = f"\nFile Encrypted 🔐\n"
            if isPdf and not(isEncrypted):
                pdfMetaData = "\n"
            # ADD META DATA TO pdfMetaData STRING
            if metaData != None:
                for i in metaData:
                    if metaData[i] != "":
                        pdfMetaData += f"`{i}: {metaData[i]}`\n"
            fileName = callbackQuery.message.reply_to_message.document.file_name
            fileSize = callbackQuery.message.reply_to_message.document.file_size
            if isPdf and not(isEncrypted):
                editedPdfReplyCb=InlineKeyboardMarkup(
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
                await callbackQuery.edit_message_text(
                    pdfInfoMsg.format(
                        fileName, await gSF(fileSize), number_of_pages
                    ) + pdfMetaData,
                    reply_markup = editedPdfReplyCb
                )
            elif isPdf and isEncrypted:
                await callbackQuery.edit_message_text(
                    encryptedMsg.format(
                        fileName, await gSF(fileSize), number_of_pages
                    ) + pdfMetaData,
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "DECRYPT 🔓",
                                    callback_data = "decrypt"
                                )
                            ]
                        ]
                    )
                )
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
    # EXCEPTION DURING FILE OPENING
    except Exception as e:
        try:
            await callbackQuery.edit_message_text(
                f"SOMETHING went WRONG.. \n\nERROR: {e}",
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "❌ - FIle error",
                                callback_data = f"error"
                            )
                        ]
                    ]
                )
            )
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass


@ILovePDF.on_callback_query(KpdfInfo)
async def _KpdfInfo(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await bot.answer_callback_query(
            callbackQuery.id,
            text = f"Total {number_of_pages} halaman",
            show_alert = True,
            cache_time = 0
        )
    except Exception:
        pass


#                                                                                  Telegram: @nabilanavab
