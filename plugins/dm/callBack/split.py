'''

█ █▄ █    █▄█ ▄▀▄ █▄ ▄█ ██▀    █▀▄ █▀▄ █▀ 
█ █ ▀█    █ █ █▀█ █ ▀ █ █▄▄    █▀  █▄▀ █▀ 
                        Dev : IlhamGUD

'''

import time
import shutil
from pdf import PROCESS
from pyromod import listen
from pyrogram import filters
from Configs.dm import Config
from plugins.checkPdf import checkPdf
from plugins.progress import progress
from pyrogram.types import ForceReply
from pyrogram import Client as InHamePDF
from PyPDF2 import PdfFileWriter, PdfFileReader
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup




# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

pdfInfoMsg = """`Apa yang ingin saya lakukan dengan file ini?`

Nama FIle: `{}`
Ukuran File: `{}`

`Jumlah Halaman: {}`✌️
"""

PDF_THUMBNAIL = Config.PDF_THUMBNAIL

# ----- ----- ----- ----- ----- ----- ----- CALLBACK SPLITTING PDF ----- ----- ----- ----- ----- ----- -----

split = filters.create(lambda _, __, query: query.data == "split")
Ksplit = filters.create(lambda _, __, query: query.data.startswith("Ksplit|"))

splitR = filters.create(lambda _, __, query: query.data == "splitR")
splitS = filters.create(lambda _, __, query: query.data == "splitS")

KsplitR = filters.create(lambda _, __, query: query.data.startswith("KsplitR|"))
KsplitS = filters.create(lambda _, __, query: query.data.startswith("KsplitS|"))



# Split pgNo (with tidak diketahui pdf page number)
@InHamePDF.on_callback_query(split)
async def _split(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Split pdf » Pages:            \n\nTotal Nomor halaman:__ `tidak diketahui`",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "With In Range",
                            callback_data = "splitR"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Single Page",
                            callback_data = "splitS"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "« Kembali «",
                            callback_data = "BTPM"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass


# Split pgNo (with known pdf page number)
@InHamePDF.on_callback_query(Ksplit)
async def _Ksplit(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"Split pdf » Pages:          \n\nTotal Nomor halaman: {number_of_pages}__ 🌟",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "With In Range",
                            callback_data = f"KsplitR|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Single Page",
                            callback_data = f"KsplitS|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "« Kembali «",
                            callback_data = f"KBTPM|{number_of_pages}"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass


# Split (with tidak diketahui pdf page number)
@InHamePDF.on_callback_query(splitR)
async def _splitROrS(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "⏳ - Sedang dalam proses"
            )
            return
        
        PROCESS.append(callbackQuery.message.chat.id)
        
        inhame = True; i = 0
        while(inhame):
            
            if i >= 5:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`5 kali percobaan, proses gagal..`"
                )
                break
            
            i += 1
            
            needPages = await bot.ask(
                text = "__Pdf Split » By Range\nSilahkan masukkan range (start:end) :__\n\n/keluar __untuk mengagalkan__",
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                filters = filters.text,
                reply_markup = ForceReply(True)
            )
            
            if needPages.text == "/keluar":
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`☑️ - Proses dibatalkan`"
                )
                break
            
            pageStartAndEnd = list(needPages.text.replace('-',':').split(':'))
            
            if len(pageStartAndEnd) > 2:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`Syntax Error: justNeedStartAndEnd `🚶"
                )
            
            elif len(pageStartAndEnd) == 2:
                start = pageStartAndEnd[0]
                end = pageStartAndEnd[1]
                
                if start.isdigit() and end.isdigit():
                
                    if (1 <= int(pageStartAndEnd[0])):
                        
                        if (int(pageStartAndEnd[0]) < int(pageStartAndEnd[1])):
                            inhame = False
                            break
                        
                        else:
                            await bot.send_message(
                                callbackQuery.message.chat.id,
                                "`Syntax Error: errorInEndingPageNumber "
                            )
                    else:
                        await bot.send_message(
                            callbackQuery.message.chat.id,
                            "`Syntax Error: errorInStartingPageNumber "
                        )
                else:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`Syntax Error: pageNumberMustBeADigit`"
                    )
            else:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`Syntax Error: noEndingPageNumber Or notADigit`"
                )
        
        if inhame == True:
            PROCESS.remove(callbackQuery.message.chat.id)
        
        if inhame == False:
            downloadMessage = await bot.send_message(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                text = "`📥 - Mendownload PDF`"
            )
            file_id = callbackQuery.message.reply_to_message.document.file_id
            fileSize = callbackQuery.message.reply_to_message.document.file_size
            
            c_time = time.time()
            downloadLoc = await bot.download_media(
                message = file_id,
                file_name = f"{callbackQuery.message.message_id}/pdf.pdf",
                progress = progress,
                progress_args = (
                    fileSize,
                    downloadMessage,
                    c_time
                )
            )
            if downloadLoc is None:
                PROCESS.remove(callbackQuery.message.chat.id)
                return
            
            await downloadMessage.edit(
                "`✅ - Download selesai`"
            )
            
            checked = await checkPdf(f'{callbackQuery.message.message_id}/pdf.pdf', callbackQuery)
            if not(checked == "pass"):
                await downloadMessage.delete()
                return
            
            splitInputPdf = PdfFileReader(f"{callbackQuery.message.message_id}/pdf.pdf")
            number_of_pages = splitInputPdf.getNumPages()
            
            if not(int(pageStartAndEnd[1]) <= int(number_of_pages)):
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`Cek nomer halaman kembali`"
                )
                PROCESS.remove(callbackQuery.message.chat.id)
                shutil.rmtree(f"{callbackQuery.message.message_id}")
                return
            
            splitOutput = PdfFileWriter()
            
            for i in range(int(pageStartAndEnd[0])-1, int(pageStartAndEnd[1])):
                splitOutput.addPage(
                    splitInputPdf.getPage(i)
                )
            
            file_path = f"{callbackQuery.message.message_id}/split.pdf"
            
            with open(file_path, "wb") as output_stream:
                splitOutput.write(output_stream)
            
            await bot.send_chat_action(
                callbackQuery.message.chat.id,
                "upload_document"
            )
            
            await bot.send_document(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.reply_to_message.message_id,
                thumb = PDF_THUMBNAIL,
                document = f"{callbackQuery.message.message_id}/split.pdf",
                caption = f"from `{pageStartAndEnd[0]}` to `{pageStartAndEnd[1]}`"
            )
            await downloadMessage.edit(
                "`✅ - Berhasil mengupload`"
            )
            
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        
    except Exception as e:
        try:
            print("SplitR: ",e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass


# Split (with tidak diketahui pdf page number)
@InHamePDF.on_callback_query(splitS)
async def _splitS(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "⏳ - Sedang dalam proses"
            )
            return
        
        PROCESS.append(callbackQuery.message.chat.id)
        
        newList = []
        inhame = True; i = 0
        while(inhame):
            
            if i >= 5:
                bot.send_message(
                    callbackQuery.message.chat.id,
                    "`5 Percobaan berakhir, silahkan gagalkan`"
                )
                break
            
            i += 1
            
            needPages = await bot.ask(
                text = "__Pdf Split » By Pages\nMasukkan Nomor halaman seperate by__ (,) :\n\n/keluar __untuk mengagalkan__",
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                filters = filters.text,
                reply_markup = ForceReply(True)
            )
            
            singlePages = list(needPages.text.replace(',',':').split(':'))
            
            if needPages.text == "/keluar":
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`☑️ - Proses dibatalkan`"
                )
                break
            
            elif 1 <= len(singlePages) <= 100:
                try:
                    for i in singlePages:
                        if i.isdigit():
                            newList.append(i)
                    if newList != []:
                        inhame = False
                        break
                    elif newList == []:
                        await bot.send_message(
                            callbackQuery.message.chat.id,
                            "`❗️ - Tidak dapat menemukan nomer`"
                        )
                        continue
                except Exception:
                    pass
            
            else:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`🔴 - Something went Wrong..`😅"
                )
        
        if inhame == True:
            PROCESS.remove(callbackQuery.message.chat.id)
        
        if inhame == False:
            downloadMessage = await bot.send_message(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                text = "`📥 - Mendownload PDF`"
            )
            file_id = callbackQuery.message.reply_to_message.document.file_id
            fileSize = callbackQuery.message.reply_to_message.document.file_size
            
            c_time = time.time()
            downloadLoc = await bot.download_media(
                message = file_id,
                file_name = f"{callbackQuery.message.message_id}/pdf.pdf",
                progress = progress,
                progress_args = (
                    fileSize,
                    downloadMessage,
                    c_time
                )
            )
            if downloadLoc is None:
                PROCESS.remove(callbackQuery.message.chat.id)
                return
            
            await downloadMessage.edit(
                "`Downloading Completed..🤞`"
            )
            
            checked = await checkPdf(f'{callbackQuery.message.message_id}/pdf.pdf', callbackQuery)
            if not(checked == "pass"):
                await downloadMessage.delete()
                return
            
            splitInputPdf = PdfFileReader(f'{callbackQuery.message.message_id}/pdf.pdf')
            number_of_pages = splitInputPdf.getNumPages()
            splitOutput = PdfFileWriter()
            
            for i in newList:
                if int(i) <= int(number_of_pages):
                    splitOutput.addPage(
                        splitInputPdf.getPage(
                            int(i)-1
                        )
                    )
            
            with open(
                f"{callbackQuery.message.message_id}/split.pdf", "wb"
            ) as output_stream:
                splitOutput.write(output_stream)
            
            await bot.send_chat_action(
                callbackQuery.message.chat.id,
                "upload_document"
            )
            
            await bot.send_document(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.reply_to_message.message_id,
                thumb = PDF_THUMBNAIL,
                document = f"{callbackQuery.message.message_id}/split.pdf",
                caption = f"Pages : `{newList}`"
            )
            
            await downloadMessage.edit(
                "`✅ - Berhasil mengupload🤞`"
            )
            
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        
    except Exception as e:
        try:
            print("splitS ;", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass


# Split (with known pdf page number)
@InHamePDF.on_callback_query(KsplitR)
async def _KsplitR(bot, callbackQuery):
    try:
        
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "⏳ - Sedang dalam proses"
            )
            return
        
        PROCESS.append(callbackQuery.message.chat.id)
        
        _, number_of_pages = callbackQuery.data.split("|")
        number_of_pages = int(number_of_pages)
        
        inhame = True; i = 0
        while(inhame):
            
            if i >= 5:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`5 Percobaan berakhir, silahkan gagalkan`"
                )
                break
            
            i += 1
            
            needPages = await bot.ask(
                text = f"__Pdf Split » By Range\nNow, Enter the range (start:end) :\nTotal halaman : __`{number_of_pages}` 🌟\n\n/keluar __untuk mengagalkan__",
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                filters = filters.text,
                reply_markup = ForceReply(True)
            )
            
            if needPages.text == "/keluar":
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`☑️ - Proses dibatalkan`"
                )
                break
            
            pageStartAndEnd = list(needPages.text.replace('-',':').split(':'))
            
            if len(pageStartAndEnd) > 2:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`Syntax Error: justNeedStartAndEnd `🚶"
                )
            
            elif len(pageStartAndEnd) == 2:
                start = pageStartAndEnd[0]
                end = pageStartAndEnd[1]
                
                if start.isdigit() and end.isdigit():
                    
                    if (int(1) <= int(start) and int(start) < number_of_pages):
                        
                        if (int(start) < int(end) and int(end) <= number_of_pages):
                            inhame = False
                            break
                        
                        else:
                            await bot.send_message(
                                callbackQuery.message.chat.id,
                                "`Syntax Error: errorInEndingPageNumber `🚶"
                            )
                    else:
                        await bot.send_message(
                            callbackQuery.message.chat.id,
                            "`Syntax Error: errorInStartingPageNumber `🚶"
                        )
                else:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`Syntax Error: pageNumberMustBeADigit` 🚶"
                    )
            else:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`Syntax Error: noSuchPageNumbers` 🚶"
                )
        
        if inhame == True:
            PROCESS.remove(callbackQuery.message.chat.id)
        
        if inhame == False:
            downloadMessage = await bot.send_message(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                text = "`📥 - Mendownload PDF`"
            )
            file_id = callbackQuery.message.reply_to_message.document.file_id
            fileSize = callbackQuery.message.reply_to_message.document.file_size
            
            c_time = time.time()
            downloadLoc = await bot.download_media(
                message = file_id,
                file_name = f"{callbackQuery.message.message_id}/pdf.pdf",
                progress = progress,
                progress_args = (
                    fileSize,
                    downloadMessage,
                    c_time
                )
            )
            
            if downloadLoc is None:
                PROCESS.remove(callbackQuery.message.chat.id)
                return
            
            await downloadMessage.edit(
                "`Downloading Completed..🤞`"
            )
            
            splitInputPdf = PdfFileReader(f"{callbackQuery.message.message_id}/pdf.pdf")
            number_of_pages = splitInputPdf.getNumPages()
            
            if not(int(pageStartAndEnd[1]) <= int(number_of_pages)):
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`1st Check the Number of pages` 😏"
                )
                PROCESS.remove(callbackQuery.message.chat.id)
                shutil.rmtree(f"{callbackQuery.message.message_id}")
                return
            
            splitOutput = PdfFileWriter()
            
            for i in range(int(pageStartAndEnd[0])-1, int(pageStartAndEnd[1])):
                splitOutput.addPage(
                    splitInputPdf.getPage(i)
                )
            
            file_path = f"{callbackQuery.message.message_id}/split.pdf"
            
            with open(file_path, "wb") as output_stream:
                splitOutput.write(output_stream)
            
            await bot.send_chat_action(
                callbackQuery.message.chat.id,
                "upload_document"
            )
            
            await bot.send_document(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.reply_to_message.message_id,
                thumb = PDF_THUMBNAIL,
                document = f"{callbackQuery.message.message_id}/split.pdf",
                caption = f"from `{pageStartAndEnd[0]}` to `{pageStartAndEnd[1]}`"
            )
            await downloadMessage.edit(
                "`✅ - Berhasil mengupload🤞`"
            )
            
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        
    except Exception as e:
        try:
            print("KsplitR :", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass


# Split (with tidak diketahui pdf page number)
@InHamePDF.on_callback_query(KsplitS)
async def _KsplitS(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "⏳ - Sedang dalam proses"
            )
            return
        
        PROCESS.append(callbackQuery.message.chat.id)
        
        _, number_of_pages = callbackQuery.data.split("|")
        
        newList = []
        inhame = True; i = 0
        while(inhame):
            
            if i >= 5:
                bot.send_message(
                    callbackQuery.message.chat.id,
                    "`5 Percobaan berakhir, silahkan gagalkan`"
                )
                break
            
            i += 1
            
            needPages = await bot.ask(
                text = f"__Pdf Split » By Pages\nEnter Nomor halaman seperate by__ (,) :\n__Total halaman : __`{number_of_pages}` 🌟\n\n/keluar __untuk mengagalkan__",
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                filters = filters.text,
                reply_markup = ForceReply(True)
            )
            
            singlePages = list(needPages.text.replace(',',':').split(':'))
            if needPages.text == "/keluar":
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`☑️ - Proses dibatalkan`"
                )
                break
            
            elif 1 <= int(len(singlePages)) and int(len(singlePages)) <= 100:
                try:
                    for i in singlePages:
                        if (i.isdigit() and int(i) <= int(number_of_pages)):
                            newList.append(i)
                    if newList == []:
                        await bot.send_message(
                             callbackQuery.message.chat.id,
                            f"`Enter Numbers less than {number_of_pages}..`😏"
                        )
                        continue
                    else:
                        inhame = False
                        break
                except Exception:
                    pass
            else:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`🔴 - Something went Wrong..`😅"
                )
        
        if inhame == True:
            PROCESS.remove(callbackQuery.message.chat.id)
        
        if inhame == False:
            downloadMessage = await bot.send_message(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                text = "`📥 - Mendownload PDF`"
            )
            
            file_id = callbackQuery.message.reply_to_message.document.file_id
            fileSize = callbackQuery.message.reply_to_message.document.file_size
            
            c_time = time.time()
            downloadLoc = await bot.download_media(
                message = file_id,
                file_name = f"{callbackQuery.message.message_id}/pdf.pdf",
                progress = progress,
                progress_args = (
                    fileSize,
                    downloadMessage,
                    c_time
                )
            )
            if downloadLoc is None:
                PROCESS.remove(callbackQuery.message.chat.id)
                return
            
            await downloadMessage.edit(
                "`Downloading Completed..🤞`"
            )
            
            splitInputPdf = PdfFileReader(f'{callbackQuery.message.message_id}/pdf.pdf')
            number_of_pages = splitInputPdf.getNumPages()
            splitOutput = PdfFileWriter()
            
            for i in newList:
                if int(i) <= int(number_of_pages):
                    splitOutput.addPage(
                        splitInputPdf.getPage(
                            int(i)-1
                        )
                    )
            
            with open(
                f"{callbackQuery.message.message_id}/split.pdf", "wb"
            ) as output_stream:
                splitOutput.write(output_stream)
            
            await bot.send_chat_action(
                callbackQuery.message.chat.id,
                "upload_document"
            )
            
            await bot.send_document(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.reply_to_message.message_id,
                thumb = PDF_THUMBNAIL,
                document = f"{callbackQuery.message.message_id}/split.pdf",
                caption = f"Pages : `{newList}`"
            )
            
            await downloadMessage.edit(
                "`✅ - Berhasil mengupload🤞`"
            )
            
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        
    except Exception as e:
        try:
            print("Ksplits: ", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass
