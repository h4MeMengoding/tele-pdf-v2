'''

█ █▄ █    █▄█ ▄▀▄ █▄ ▄█ ██▀    █▀▄ █▀▄ █▀ 
█ █ ▀█    █ █ █▀█ █ ▀ █ █▄▄    █▀  █▄▀ █▀ 
                        Dev : IlhamGUD

'''

from pdf import invite_link
from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as InHame
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup





#--------------->
#--------> LOCAL VARIABLES
#------------------->

welcomeMsg = """Halo [{}](tg://user?id={}) 👋 Bot ini akan membantu Anda melakukan banyak hal dengan pdf 

Fitur utama yang tersedia:
➤ `Convert images to PDF`
➤ `Convert PDF to images`
➤ `Convert files to pdf`

Note : Mungkin ada beberapa fitur yang tidak dapat digunakan (bug), semua sedang dalam development. Terimakasih
"""


UCantUse = "Kamu telah di-BAN karena melanggar ketentuan"


forceSubMsg = """Tunggu [{}](tg://user?id={})..!!

Karena alasan traffic server maka hanya Anggota channel yang Dapat Menggunakan
    
Anda diwajibkan untuk bergabung kedalam channel.

Klik "refresh" jika sudah bergabung.. 
"""


aboutDev = """Dev tampang jangan lupa diisi -zeyy"""


exploreBotEdit = """
‼️ - SEDANG DALAM PROSES PENGEMBANGAN
"""


jikaboong = """Cie boong, masuk channel dulu baru bisa gunain yaa..."""

#--------------->
#--------> config vars
#------------------->

UPDATE_CHANNEL=Config.UPDATE_CHANNEL
BANNED_USERS=Config.BANNED_USERS
ADMIN_ONLY=Config.ADMIN_ONLY
ADMINS=Config.ADMINS

#--------------->
#--------> /start (START MESSAGE)
#------------------->


@InHame.on_message(filters.private & ~filters.edited & filters.command(["start"]))
async def start(bot, message):
        global invite_link
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        # CHECK IF USER BANNED, ADMIN ONLY..
        if (message.chat.id in BANNED_USERS) or (
            (ADMIN_ONLY) and (message.chat.id not in ADMINS)
        ):
            await bot.send_message(
                message.chat.id, UCantUse
            )
            return
        # CHECK USER IN CHANNEL (IF UPDATE_CHANNEL ADDED)
        if UPDATE_CHANNEL:
            try:
                await bot.get_chat_member(
                    str(UPDATE_CHANNEL), message.chat.id
                )
            except Exception:
                if invite_link == None:
                    invite_link = await bot.create_chat_invite_link(
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
                                    url = invite_link.invite_link
                                ),
                                InlineKeyboardButton(
                                    "REFRESH",
                                    callback_data = "refresh"
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    "CARA MENGGUNAKAN",
                                    url= "https://telegra.ph/Cara-Menyimpan-PDF-ke-Storage-02-20-2"
                                )
                            ]
                        ]
                    )
                )
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = message.message_id
                )
                return
        
        await bot.send_message(
            message.chat.id,
            welcomeMsg.format(
                message.from_user.first_name,
                message.chat.id
            ),
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "FITUR LAINNYA",
                            callback_data = "exploreBot"
                        ),
                        InlineKeyboardButton(
                            "TUTUP",
                            callback_data = "close"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "CARA MENGGUNAKAN",
                            url= "https://telegra.ph/Cara-Menyimpan-PDF-ke-Storage-02-20-2"
                        )
                    ]
                ]
            )
        )
        # DELETES /start MESSAGE
        await bot.delete_messages(
            chat_id = message.chat.id,
            message_ids = message.message_id
        )


#--------------->
#--------> START CALLBACKS
#------------------->


strtDevEdt = filters.create(lambda _, __, query: query.data == "strtDevEdt")
exploreBot = filters.create(lambda _, __, query: query.data == "exploreBot")
refresh = filters.create(lambda _, __, query: query.data == "refresh")
close = filters.create(lambda _, __, query: query.data == "close")
back = filters.create(lambda _, __, query: query.data == "back")



@InHame.on_callback_query(strtDevEdt)
async def _strtDevEdt(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            aboutDev,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "BERANDA",
                            callback_data = "back"
                        ),
                        InlineKeyboardButton(
                            "TUTUP",
                            callback_data = "close"
                        )
                    ]
                ]
            )
        )
        return
    except Exception as e:
        print(e)


@InHame.on_callback_query(exploreBot)
async def _exploreBot(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            exploreBotEdit,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "BERANDA",
                            callback_data = "back"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "TUTUP",
                            callback_data = "close"
                        )
                    ]
                ]
            )
        )
        return
    except Exception as e:
        print(e)


@InHame.on_callback_query(back)
async def _back(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            welcomeMsg.format(
                callbackQuery.from_user.first_name,
                callbackQuery.message.chat.id
            ),
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "FITUR LAINNYA",
                            callback_data = "exploreBot"
                        ),
                        InlineKeyboardButton(
                            "TUTUP",
                            callback_data = "close"
                        )
                    ]
                ]
            )
        )
        return
    except Exception as e:
        print(e)


@InHame.on_callback_query(refresh)
async def _refresh(bot, callbackQuery):
    try:
        # CHECK USER IN CHANNEL (REFRESH CALLBACK)
        await bot.get_chat_member(
            str(UPDATE_CHANNEL),
            callbackQuery.message.chat.id
        )
        # IF USER NOT MEMBER (ERROR FROM TG, EXECUTE EXCEPTION)
        await callbackQuery.edit_message_text(
            welcomeMsg.format(
                callbackQuery.from_user.first_name,
                callbackQuery.message.chat.id
            ),
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "FITUR LAINNYA",
                            callback_data = "exploreBot"
                        ),
                        InlineKeyboardButton(
                            "TUTUP",
                            callback_data = "close"
                        )
                    ]
                ]
            )
        )
    except Exception:
        try:
            # IF NOT USER ALERT MESSAGE (AFTER CALLBACK)
            await bot.answer_callback_query(
                callbackQuery.id,
                text = jikaboong,
                show_alert = True,
                cache_time = 0
            )
        except Exception as e:
            print(e)


@InHame.on_callback_query(close)
async def _close(bot, callbackQuery):
    try:
        await bot.delete_messages(
            chat_id = callbackQuery.message.chat.id,
            message_ids = callbackQuery.message.message_id
        )
        return
    except Exception as e:
        print(e)


# Copyright InHame Dev
