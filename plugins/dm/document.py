# fileName : plugins/dm/document.py
# copyright ©️ 2021 nabilanavab




import os
import fitz
import shutil
import convertapi
from pdf import PDF
from PIL import Image
from time import sleep
from pdf import invite_link
from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as ILovePDF
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup




#--------------->
#--------> convertAPI instance
#------------------->

if Config.CONVERT_API is not None:
    convertapi.api_secret = os.getenv("CONVERT_API")

#--------------->
#--------> MAXIMUM FILE SIZE (IF IN config var.)
#------------------->

if Config.MAX_FILE_SIZE:
    MAX_FILE_SIZE=int(os.getenv("MAX_FILE_SIZE"))
    MAX_FILE_SIZE_IN_kiB=MAX_FILE_SIZE * (10 **6 )
else:
    MAX_FILE_SIZE=False


PDF_THUMBNAIL=Config.PDF_THUMBNAIL

#--------------->
#--------> FILES TO PDF SUPPORTED CODECS
#------------------->

suprtedFile = [
    ".jpg", ".jpeg", ".png"
]                                       # Img to pdf file support

suprtedPdfFile = [
    ".epub", ".xps", ".oxps",
    ".cbz", ".fb2"
]                                      # files to pdf (zero limits)

suprtedPdfFile2 = [
    ".csv", ".doc", ".docx", ".dot",
    ".dotx", ".log", ".mpp", ".mpt",
    ".odt", ".pot", ".potx", ".pps",
    ".ppsx", ".ppt", ".pptx", ".pub",
    ".rtf", ".txt", ".vdx", ".vsd",
    ".vsdx", ".vst", ".vstx", ".wpd",
    ".wps", ".wri", ".xls", ".xlsb",
    ".xlsx", ".xlt", ".xltx", ".xml"
]                                       # file to pdf (ConvertAPI limit)

#--------------->
#--------> LOCAL VARIABLES
#------------------->

UCantUse = "Kamu telah di-BAN karena melanggar ketentuan"


pdfReplyMsg = """`Quick Informasi`

Nama File : `{}`
Ukuran File : `{}`"""


bigFileUnSupport = """Karena Overload, bot hanya mendukung file {}mb PDF

`silahkan kirim file kurang dari {}mb`"""


imageAdded = """`✅ - Berhasil Menambahkan {} halaman ke pdf`
"""


errorEditMsg = """⛔️ - Something went wrong

ERROR: `{}`
"""


feedbackMsg = """
[Tulis feedback 📋](https://tellonym.me/Developer_InHame)
"""


forceSubMsg = """Tunggu [{}](tg://user?id={})..!!

Karena alasan traffic server maka hanya Anggota channel yang Dapat Menggunakan
    
Anda diwajibkan untuk bergabung kedalam channel.

Klik "refresh" jika sudah bergabung.. 
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
#--------> PDF REPLY BUTTON
#------------------->

pdfReply=InlineKeyboardMarkup(
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


#--------------->
#--------> Config var.
#------------------->

UPDATE_CHANNEL=Config.UPDATE_CHANNEL
BANNED_USERS=Config.BANNED_USERS
ADMIN_ONLY=Config.ADMIN_ONLY
ADMINS=Config.ADMINS

#--------------->
#--------> REPLY TO DOCUMENTS/FILES
#------------------->


@ILovePDF.on_message(filters.private & filters.document & ~filters.edited)
async def documents(bot, message):
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
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "BERGABUNG",
                                    url=invite_link.invite_link
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    "REFRESH",
                                    callback_data="refresh"
                                )
                            ]
                        ]
                    )
                )
                return
        # CHECKS IF USER BANNED/ADMIN..
        if (message.chat.id in BANNED_USERS) or (
            (ADMIN_ONLY) and (message.chat.id not in ADMINS)
        ):
            await message.reply_text(
                UCantUse,
                reply_markup=button
            )
            return
        
        isPdfOrImg = message.document.file_name        # file name
        fileSize = message.document.file_size          # file size
        fileNm, fileExt = os.path.splitext(isPdfOrImg) # seperate name & extension
        
        # REPLY TO LAGE FILES/DOCUMENTS
        if MAX_FILE_SIZE and fileSize >= int(MAX_FILE_SIZE_IN_kiB):
            await message.reply_text(
                bigFileUnSupport.format(MAX_FILE_SIZE, MAX_FILE_SIZE), quote=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                             InlineKeyboardButton(
                                "CHAT DEV",
                                url="https://t.me/ilhamshff"
                            )
                        ]
                    ]
                )
            )
            return
        
        # IMAGE AS FILES (ADDS TO PDF FILE)
        elif fileExt.lower() in suprtedFile:
            try:
                imageDocReply = await message.reply_text(
                    "`⏳- Mengunduh Gambar Anda`", quote=True
                )
                if not isinstance(PDF.get(message.chat.id), list):
                    PDF[message.chat.id]=[]
                await message.download(
                    f"{message.chat.id}/{message.chat.id}.jpg"
                )
                img = Image.open(
                    f"{message.chat.id}/{message.chat.id}.jpg"
                ).convert("RGB")
                PDF[message.chat.id].append(img)
                await imageDocReply.edit(
                    imageAdded.format(len(PDF[message.chat.id]))
                )
            except Exception as e:
                await imageDocReply.edit(
                    errorEditMsg.format(e)
                )
            
        # REPLY TO .PDF FILE EXTENSION
        elif fileExt.lower() == ".pdf":
            try:
                pdfMsgId = await message.reply_text(
                    "⏳- Memproses", quote=True
                )
                sleep(0.5)
                await pdfMsgId.edit(
                    text=pdfReplyMsg.format(
                        isPdfOrImg, await gSF(fileSize)
                    ),
                    reply_markup=pdfReply
                )
            except Exception:
                pass
        
        # FILES TO PDF (PYMUPDF/FITZ)
        elif fileExt.lower() in suprtedPdfFile:
            try:
                pdfMsgId = await message.reply_text(
                    "`⏳ - Mengunduh file anda`", quote=True
                )
                await message.download(
                    f"{message.message_id}/{isPdfOrImg}"
                )
                await pdfMsgId.edit(
                    "`🖨 - Membuat pdf`"
                )
                Document=fitz.open(
                    f"{message.message_id}/{isPdfOrImg}"
                )
                b=Document.convert_to_pdf()
                pdf=fitz.open("pdf", b)
                pdf.save(
                    f"{message.message_id}/{fileNm}.pdf",
                    garbage=4,
                    deflate=True,
                )
                pdf.close()
                await pdfMsgId.edit(
                    "`📤 - Mengirim file`"
                )
                await bot.send_chat_action(
                    message.chat.id, "upload_document"
                )
                await message.reply_document(
                    document=open(f"{message.message_id}/{fileNm}.pdf", "rb"),
                    thumb=PDF_THUMBNAIL,
                    caption=f"`Converted: {fileExt} to pdf`",
                    quote=True
                )
                await pdfMsgId.delete()
                shutil.rmtree(f"{message.message_id}")
                sleep(5)
                await bot.send_chat_action(
                    message.chat.id, "typing"
                )
                await bot.send_message(
                    message.chat.id, feedbackMsg,
                    disable_web_page_preview = True
                )
            except Exception as e:
                try:
                    shutil.rmtree(f"{message.message_id}")
                    await pdfMsgId.edit(
                        errorEditMsg.format(e)
                    )
                except Exception:
                    pass
        
        # FILES TO PDF (CONVERTAPI)
        elif fileExt.lower() in suprtedPdfFile2:
            if os.getenv("CONVERT_API") is None:
                pdfMsgId = await message.reply_text(
                    "`Error : API key tidak ditambahkan, silahkan hubungi developer`",
                    quote=True
                )
                return
            else:
                try:
                    pdfMsgId = await message.reply_text(
                        "`⏳ - Mengunduh file anda`", quote=True
                    )
                    await message.download(
                        f"{message.message_id}/{isPdfOrImg}"
                    )
                    await pdfMsgId.edit(
                        "`🖨 - Membuat pdf`"
                    )
                    try:
                        await convertapi.convert(
                            "pdf",
                            {
                                "File": f"{message.message_id}/{isPdfOrImg}"
                            },
                            from_format = fileExt[1:],
                        ).save_files(
                            f"{message.message_id}/{fileNm}.pdf"
                        )
                    except Exception:
                        try:
                            shutil.rmtree(f"{message.message_id}")
                            await pdfMsgId.edit(
                                "ConvertAPI limit reaches.. contact Owner"
                            )
                            return
                        except Exception:
                            pass
                    await bot.send_chat_action(
                        message.chat.id, "upload_document"
                    )
                    await message.reply_document(
                        document=open(f"{message.message_id}/{fileNm}.pdf", "rb"),
                        thumb=PDF_THUMBNAIL,
                        caption=f"`Converted: {fileExt} to pdf`",
                        quote=True
                    )
                    await pdfMsgId.delete()
                    shutil.rmtree(f"{message.message_id}")
                    sleep(5)
                    await bot.send_chat_action(
                        message.chat.id, "typing"
                    )
                    await bot.send_message(
                        message.chat.id, feedbackMsg,
                        disable_web_page_preview=True
                    )
                except Exception:
                    pass
        
        # UNSUPPORTED FILES
        else:
            try:
                await message.reply_text(
                    "`File tidak didukung..`", quotes=True
                )
            except Exception:
                pass
    
    except Exception as e:
        print("plugins/dm/document : ", e)


#                                                                                  Telegram: @nabilanavab
