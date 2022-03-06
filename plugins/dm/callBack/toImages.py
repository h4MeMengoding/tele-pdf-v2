'''

█ █▄ █    █▄█ ▄▀▄ █▄ ▄█ ██▀    █▀▄ █▀▄ █▀ 
█ █ ▀█    █ █ █▀█ █ ▀ █ █▄▄    █▀  █▄▀ █▀ 
                        Dev : IlhamGUD

'''

import os
import fitz
import time
import shutil
from PIL import Image
from pdf import PROCESS
from pyromod import listen
from pyrogram import filters
from Configs.dm import Config
from plugins.checkPdf import checkPdf
from plugins.progress import progress
from pyrogram.types import ForceReply
from pyrogram import Client as InHamePDF
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InputMediaPhoto, InputMediaDocument
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup




#--------------->
#--------> LOCAL VARIABLES
#------------------->

PDF_THUMBNAIL = Config.PDF_THUMBNAIL

mediaDoc = {}
media = {}

#--------------->
#--------> PDF TO IMAGES
#------------------->

KcbExtract = ["KIA|", "KIR|", "KDA|", "KDR|", "KIS|", "KDS|"]
EXTRACT = filters.create(lambda _, __, query: query.data in ["IA", "DA", "IR", "DR", "IS", "DS"])
KEXTRACT = filters.create(lambda _, __, query: query.data.startswith(tuple(KcbExtract)))


# Extract pgNo (with tidak diketahui pdf page number)
@InHamePDF.on_callback_query(EXTRACT)
async def _EXTRACT(bot, callbackQuery):
    try:
        # CALLBACK DATA
        data = callbackQuery.data
        # CHECK USER PROCESS
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "⏳ - Sedang dalam proses"
            )
            return
        # ADD USER TO PROCESS
        PROCESS.append(callbackQuery.message.chat.id)
        
        # ACCEPTING PAGE NUMBER
        if data in ["IA", "DA"]:
            inhame = False
        # RANGE (START:END)
        elif data in ["IR", "DR"]:
            inhame = True; i = 0
            # 5 EXCEPTION, BREAK MERGE PROCESS
            while(inhame):
                if i >= 5:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`5 Percobaan berakhir, silahkan gagalkan`"
                    )
                    break
                i += 1
                # PYROMOD ADD-ON (PG NO REQUEST)
                needPages = await bot.ask(
                    text = "__Pdf - Img›Doc » Pages:\nMasukkan rentang (range) (start:end) :__\n\n/keluar __untuk membatalkan__",
                    chat_id = callbackQuery.message.chat.id,
                    reply_to_message_id = callbackQuery.message.message_id,
                    filters = filters.text,
                    reply_markup = ForceReply(True)
                )
                # EXIT PROCESS
                if needPages.text == "/keluar":
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`☑️ - Proses dibatalkan`"
                    )
                    break
                # SPLIT STRING TO START & END
                pageStartAndEnd = list(needPages.text.replace('-',':').split(':'))
                # IF STRING HAVE MORE THAN 2 LIMITS
                if len(pageStartAndEnd) > 2:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`Syntax Error: justNeedStartAndEnd `🚶"
                    )
                # CORRECT FORMAT
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
                            "`Syntax Error: pageNumberMustBeADigit` 🧠"
                        )
                # ERPOR MESSAGE
                else:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`Syntax Error: noEndingPageNumber Or notADigit` 🚶"
                    )
        # SINGLE PAGES
        else:
            newList = []
            inhame = True; i = 0
            # 5 REQUEST LIMIT
            while(inhame):
                if i >= 5:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`5 Percobaan berakhir, silahkan gagalkan`"
                    )
                    break
                i += 1
                # PYROMOD ADD-ON
                needPages = await bot.ask(
                    text = "__Pdf - Img›Doc » Pages:\nNow, Enter the Nomor halaman seperated by__ (,) :\n\n/keluar __untuk membatalkan__",
                    chat_id = callbackQuery.message.chat.id,
                    reply_to_message_id = callbackQuery.message.message_id,
                    filters = filters.text,
                    reply_markup = ForceReply(True)
                )
                # SPLIT PAGE NUMBERS (,)
                singlePages = list(needPages.text.replace(',',':').split(':'))
                # PROCESS CANCEL
                if needPages.text == "/keluar":
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`☑️ - Proses dibatalkan`"
                    )
                    break
                # PAGE NUMBER LESS THAN 100
                elif 1 <= len(singlePages) <= 100:
                    # CHECK IS PAGE NUMBER A DIGIT(IF ADD TO A NEW LIST)
                    for i in singlePages:
                        if i.isdigit():
                            newList.append(i)
                    if newList != []:
                        inhame = False
                        break
                    # AFTER SORTING (IF NO DIGIT PAGES RETURN)
                    elif newList == []:
                        await bot.send_message(
                            callbackQuery.message.chat.id,
                            "`❗️ - Tidak dapat menemukan nomer`"
                        )
                        continue
                else:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`🔴 - Something went Wrong..`"
                    )
        if inhame == True:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        if inhame == False:
            # DOWNLOAD MESSAGE
            downloadMessage = await bot.send_message(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                text = "`📥 - Mendownload PDF`"
            )
            file_id = callbackQuery.message.reply_to_message.document.file_id
            fileSize = callbackQuery.message.reply_to_message.document.file_size
            # DOWNLOAD PROGRESS
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
            # CHECK DOWNLOAD COMPLETED/CANCELLED
            if downloadLoc is None:
                PROCESS.remove(callbackQuery.message.chat.id)
                return
            # CHECK PDF CODEC, ENCRYPTION..
            checked = await checkPdf(
                f'{callbackQuery.message.message_id}/pdf.pdf', callbackQuery
            )
            if not(checked == "pass"):
                await downloadMessage.delete()
                return
            # OPEN PDF WITH FITZ
            doc = fitz.open(f'{callbackQuery.message.message_id}/pdf.pdf')
            number_of_pages = doc.pageCount
            if data in ["IA", "DA"]:
                pageStartAndEnd = [1, int(number_of_pages)]
            if data in ["IR", "DR"]:
                if not(int(pageStartAndEnd[1]) <= int(number_of_pages)):
                    await bot.edit_message_text(
                        chat_id = callbackQuery.message.chat.id,
                        message_id = downloadMessage.message_id,
                        text = f"`PDF hanya mempunyai {number_of_pages} halaman`"
                    )
                    PROCESS.remove(callbackQuery.message.chat.id)
                    shutil.rmtree(f"{callbackQuery.message.message_id}")
                    return
            zoom = 2
            mat = fitz.Matrix(zoom, zoom)
            if data in ["IA", "DA", "IR", "DR"]:
                if int(int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])) >= 11:
                    await bot.pin_chat_message(
                        chat_id = callbackQuery.message.chat.id,
                        message_id = downloadMessage.message_id,
                        disable_notification = True,
                        both_sides = True
                    )
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = downloadMessage.message_id,
                    text = f"`📄 - Total halaman: {int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])}`"
                )
                totalPgList = range(int(pageStartAndEnd[0]), int(pageStartAndEnd[1])+1)
                cnvrtpg = 0
                for i in range(0, len(totalPgList), 10):
                    pgList = totalPgList[i:i+10]
                    os.mkdir(f'{callbackQuery.message.message_id}/pgs')
                    for pageNo in pgList:
                        page = doc.loadPage(pageNo-1)
                        pix = page.getPixmap(matrix = mat)
                        cnvrtpg += 1
                        if cnvrtpg % 5 == 0:
                            await bot.edit_message_text(
                                chat_id = callbackQuery.message.chat.id,
                                message_id = downloadMessage.message_id,
                                text = f"`Converted: {cnvrtpg}/{int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])} halaman..`"
                            )
                        if callbackQuery.message.chat.id not in PROCESS:
                            try:
                                await bot.edit_message_text(
                                    chat_id = callbackQuery.message.chat.id,
                                    message_id = downloadMessage.message_id,
                                    text = f"`Dibatalkan pada {cnvrtpg}/{int(int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0]))} halaman..`"
                                )
                                shutil.rmtree(f'{callbackQuery.message.message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        with open(
                            f'{callbackQuery.message.message_id}/pgs/{pageNo}.jpg','wb'
                        ):
                            pix.writePNG(f'{callbackQuery.message.message_id}/pgs/{pageNo}.jpg')
                    try:
                        await bot.edit_message_text(
                            chat_id = callbackQuery.message.chat.id,
                            message_id = downloadMessage.message_id,
                            text = f"`⏳ - Menyiapkan gambar`"
                        )
                    except Exception:
                        pass
                    directory = f'{callbackQuery.message.message_id}/pgs'
                    imag = [os.path.join(directory, file) for file in os.listdir(directory)]
                    imag.sort(key=os.path.getctime)
                    media[callbackQuery.message.chat.id] = []
                    mediaDoc[callbackQuery.message.chat.id] = []
                    LrgFileNo = 1
                    for file in imag:
                        if os.path.getsize(file) >= 1000000:
                            picture = Image.open(file)
                            CmpImg = f'{callbackQuery.message.message_id}/pgs/temp{LrgFileNo}.jpeg'
                            picture.save(
                                CmpImg,
                                "JPEG",
                                optimize=True,
                                quality = 75
                            )
                            LrgFileNo += 1
                            file = CmpImg
                            if os.path.getsize(CmpImg) >= 1000000:
                                picture = Image.open(CmpImg)
                                CmpCmpImg = f'{callbackQuery.message.message_id}/pgs/temP{LrgFileNo}.jpeg'
                                picture.save(
                                    CmpCmpImg,
                                    "JPEG",
                                    optimize=True,
                                    quality=75
                                )
                                file = CmpCmpImg
                                if os.path.getsize(CmpCmpImg) >= 1000000:
                                    picture = Image.open(CmpCmpImg)
                                    CmpCmpCmpImg = f'{callbackQuery.message.message_id}/pgs/teMP{LrgFileNo}.jpeg'
                                    picture.save(
                                        CmpCmpCmpImg,
                                        "JPEG",
                                        optimize=True,
                                        quality=75
                                    )
                                    file = CmpCmpCmpImg
                                    if os.path.getsize(CmpCmpImg) >= 1000000:
                                        continue
                                    else:
                                        media[
                                            callbackQuery.message.chat.id
                                        ].append(
                                            InputMediaPhoto(media = file)
                                        )
                                        mediaDoc[
                                            callbackQuery.message.chat.id
                                        ].append(
                                            InputMediaDocument(media = file)
                                        )
                                        continue
                                else:
                                    media[
                                        callbackQuery.message.chat.id
                                    ].append(
                                        InputMediaPhoto(media = file)
                                    )
                                    mediaDoc[
                                        callbackQuery.message.chat.id
                                    ].append(
                                        InputMediaDocument(media = file)
                                    )
                                    continue
                            else:
                                media[
                                    callbackQuery.message.chat.id
                                ].append(
                                    InputMediaPhoto(media = file)
                                )
                                mediaDoc[
                                    callbackQuery.message.chat.id
                                ].append(
                                    InputMediaDocument(media = file)
                                )
                                continue
                        media[
                            callbackQuery.message.chat.id
                        ].append(
                            InputMediaPhoto(media = file)
                        )
                        mediaDoc[
                            callbackQuery.message.chat.id
                        ].append(
                            InputMediaDocument(media = file)
                        )
                    await bot.edit_message_text(
                        chat_id = callbackQuery.message.chat.id,
                        message_id = downloadMessage.message_id,
                        text = f"`Mengupload: {cnvrtpg}/{int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])} halaman..`"
                    )
                    if data in ["IA", "IR"]:
                        if callbackQuery.message.chat.id not in PROCESS:
                            try:
                                shutil.rmtree(f'{callbackQuery.message.message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        await bot.send_chat_action(
                            callbackQuery.message.chat.id, "upload_photo"
                        )
                        try:
                            await bot.send_media_group(
                                callbackQuery.message.chat.id,
                                media[callbackQuery.message.chat.id]
                            )
                        except Exception:
                            del media[callbackQuery.message.chat.id]
                            del mediaDoc[callbackQuery.message.chat.id]
                    if data in ["DA", "DR"]:
                        if callbackQuery.message.chat.id not in PROCESS:
                            try:
                                shutil.rmtree(f'{callbackQuery.message.message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        await bot.send_chat_action(
                            callbackQuery.message.chat.id, "upload_document"
                        )
                        try:
                            await bot.send_media_group(
                                callbackQuery.message.chat.id,
                                mediaDoc[callbackQuery.message.chat.id]
                            )
                        except Exception:
                            del mediaDoc[callbackQuery.message.chat.id]
                            del media[callbackQuery.message.chat.id]
                    shutil.rmtree(f'{callbackQuery.message.message_id}/pgs')
                PROCESS.remove(callbackQuery.message.chat.id)
                doc.close()
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = downloadMessage.message_id,
                    text = f'`✅ - Berhasil mengupload `'
                )
                shutil.rmtree(f'{callbackQuery.message.message_id}')
            if data in ["IS", "DS"]:
                if int(len(newList)) >= 11:
                    await bot.pin_chat_message(
                        chat_id = callbackQuery.message.chat.id,
                        message_id = downloadMessage.message_id,
                        disable_notification = True,
                        both_sides = True
                    )
                totalPgList = []
                for i in newList:
                    if 1 <= int(i) <= number_of_pages:
                        totalPgList.append(i)
                if len(totalPgList) < 1:
                    await bot.edit_message_text(
                        chat_id = callbackQuery.message.chat.id,
                        message_id = downloadMessage.message_id,
                        text = f"`PDF hanya mempunyai {number_of_pages} halaman`"
                    )
                    PROCESS.remove(callbackQuery.message.chat.id)
                    shutil.rmtree(f'{callbackQuery.message.message_id}')
                    doc.close()
                    return
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = downloadMessage.message_id,
                    text = f"`📄 - Total halaman: {len(totalPgList)}`"
                )
                cnvrtpg = 0
                for i in range(0, len(totalPgList), 10):
                    pgList = totalPgList[i:i+10]
                    os.mkdir(f'{callbackQuery.message.message_id}/pgs')
                    for pageNo in pgList:
                        if int(pageNo) <= int(number_of_pages):
                            page = doc.loadPage(int(pageNo)-1)
                            pix = page.getPixmap(matrix = mat)
                        else:
                            continue
                        cnvrtpg += 1
                        if cnvrtpg % 5 == 0:
                            await bot.edit_message_text(
                                chat_id = callbackQuery.message.chat.id,
                                message_id = downloadMessage.message_id,
                                text = f"`Converted: {cnvrtpg}/{len(totalPgList)} halaman..`"
                            )
                        if callbackQuery.message.chat.id not in PROCESS:
                            try:
                                await bot.edit_message_text(
                                    chat_id = callbackQuery.message.chat.id,
                                    message_id = downloadMessage.message_id,
                                    text = f"`Dibatalkan pada {cnvrtpg}/{len(totalPgList)} halaman..`"
                                )
                                shutil.rmtree(f'{callbackQuery.message.message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        with open(
                            f'{callbackQuery.message.message_id}/pgs/{pageNo}.jpg','wb'
                        ):
                            pix.writePNG(f'{callbackQuery.message.message_id}/pgs/{pageNo}.jpg')
                    try:
                        await bot.edit_message_text(
                            chat_id = callbackQuery.message.chat.id,
                            message_id = downloadMessage.message_id,
                            text = f"`⏳ - Menyiapkan gambar`"
                        )
                    except Exception:
                        pass
                    directory = f'{callbackQuery.message.message_id}/pgs'
                    imag = [os.path.join(directory, file) for file in os.listdir(directory)]
                    imag.sort(key=os.path.getctime)
                    media[callbackQuery.message.chat.id] = []
                    mediaDoc[callbackQuery.message.chat.id] = []
                    LrgFileNo = 1
                    for file in imag:
                        if os.path.getsize(file) >= 1000000:
                            picture = Image.open(file)
                            CmpImg = f'{callbackQuery.message.message_id}/pgs/temp{LrgFileNo}.jpeg'
                            picture.save(
                                CmpImg,
                                "JPEG",
                                optimize=True,
                                quality = 75
                            ) 
                            LrgFileNo += 1
                            file = CmpImg
                            if os.path.getsize(CmpImg) >= 1000000:
                                picture = Image.open(CmpImg)
                                CmpCmpImg = f'{callbackQuery.message.message_id}/pgs/temP{LrgFileNo}.jpeg'
                                picture.save(
                                    CmpCmpImg,
                                    "JPEG",
                                    optimize=True,
                                    quality=75
                                )
                                file = CmpCmpImg
                                if os.path.getsize(CmpCmpImg) >= 1000000:
                                    picture = Image.open(CmpCmpImg)
                                    CmpCmpCmpImg = f'{callbackQuery.message.message_id}/pgs/teMP{LrgFileNo}.jpeg'
                                    picture.save(
                                        CmpCmpCmpImg,
                                        "JPEG",
                                        optimize=True,
                                        quality=75
                                    )
                                    file = CmpCmpCmpImg
                                    if os.path.getsize(CmpCmpImg) >= 1000000:
                                        continue
                                    else:
                                        media[
                                            callbackQuery.message.chat.id
                                        ].append(
                                            InputMediaPhoto(media = file)
                                        )
                                        mediaDoc[
                                            callbackQuery.message.chat.id
                                        ].append(
                                            InputMediaDocument(media = file)
                                        )
                                        continue
                                else:
                                    media[
                                        callbackQuery.message.chat.id
                                    ].append(
                                        InputMediaPhoto(media = file)
                                    )
                                    mediaDoc[
                                        callbackQuery.message.chat.id
                                    ].append(
                                        InputMediaDocument(media = file)
                                    )
                                    continue
                            else:
                                media[
                                    callbackQuery.message.chat.id
                                ].append(
                                    InputMediaPhoto(media = file)
                                )
                                mediaDoc[
                                    callbackQuery.message.chat.id
                                ].append(
                                    InputMediaDocument(media = file)
                                )
                                continue
                        media[
                            callbackQuery.message.chat.id
                        ].append(
                            InputMediaPhoto(media = file)
                        )
                        mediaDoc[
                            callbackQuery.message.chat.id
                        ].append(
                            InputMediaDocument(media = file)
                        )
                    await bot.edit_message_text(
                        chat_id = callbackQuery.message.chat.id,
                        message_id = downloadMessage.message_id,
                        text = f"`Mengupload: {cnvrtpg}/{len(totalPgList)} halaman..`"
                    )
                    if data == "IS":
                        if callbackQuery.message.chat.id not in PROCESS:
                            try:
                                shutil.rmtree(f'{callbackQuery.message.message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        await bot.send_chat_action(
                            callbackQuery.message.chat.id, "upload_photo"
                        )
                        try:
                            await bot.send_media_group(
                                callbackQuery.message.chat.id,
                                media[callbackQuery.message.chat.id]
                            )
                        except Exception:
                            del media[callbackQuery.message.chat.id]
                            del mediaDoc[callbackQuery.message.chat.id]
                    if data == "DS":
                        if callbackQuery.message.chat.id not in PROCESS:
                            try:
                                shutil.rmtree(f'{callbackQuery.message.message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        await bot.send_chat_action(
                            callbackQuery.message.chat.id, "upload_document"
                        )
                        try:
                            await bot.send_media_group(
                                callbackQuery.message.chat.id,
                                mediaDoc[callbackQuery.message.chat.id]
                            )
                        except Exception:
                            del mediaDoc[callbackQuery.message.chat.id]
                            del media[callbackQuery.message.chat.id]
                    shutil.rmtree(f'{callbackQuery.message.message_id}/pgs')
                PROCESS.remove(callbackQuery.message.chat.id)
                doc.close()
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = downloadMessage.message_id,
                    text = f'`✅ - Berhasil mengupload `🏌️'
                )
                shutil.rmtree(f'{callbackQuery.message.message_id}')
    except Exception as e:
        try:
            print("image: ", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f'{callbackQuery.message.message_id}')
        except Exception:
            pass


# Extract pgNo (with known pdf page number)
@InHamePDF.on_callback_query(KEXTRACT)
async def _KEXTRACT(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "⏳ - Sedang dalam proses"
            )
            return
        data = callbackQuery.data[:3]
        _, number_of_pages = callbackQuery.data.split("|")
        PROCESS.append(callbackQuery.message.chat.id)
        if data in ["KIA", "KDA"]:
            inhame = False
        elif data in ["KIR", "KDR"]:
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
                    text = "__Pdf - Img›Doc » Pages:\nMasukkan rentang (range) (start:end) :__\n\n/keluar __untuk membatalkan__",
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
                        "`Syntax Error: justNeedStartAndEnd `"
                    )
                elif len(pageStartAndEnd) == 2:
                    start = pageStartAndEnd[0]
                    end = pageStartAndEnd[1]
                    if start.isdigit() and end.isdigit():
                        if (1 <= int(pageStartAndEnd[0])):
                            if int(pageStartAndEnd[0]) < int(pageStartAndEnd[1]) and int(pageStartAndEnd[1]) <= int(number_of_pages):
                                inhame = False
                                break
                            else:
                                await bot.send_message(
                                    callbackQuery.message.chat.id,
                                    "`Syntax Error: errorInEndingPageNumber `"
                                )
                        else:
                            await bot.send_message(
                                callbackQuery.message.chat.id,
                                "`Syntax Error: errorInStartingPageNumber `"
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
        elif data in ["KIS", "KDS"]:
            newList = []
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
                    text = "__Pdf - Img›Doc » Pages:\nMasukkan nomor halaman seperated by__ (,) :\n\n/keluar __untuk membatalkan__",
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
                    for i in singlePages:
                        if i.isdigit() and int(i) <= int(number_of_pages):
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
                else:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`100 page is enough..`"
                    )
        if inhame == True:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        if inhame == False:
            downloadMessage = await bot.send_message(
                chat_id = callbackQuery.message.chat.id,
                reply_to_message_id = callbackQuery.message.message_id,
                text = "`📥 - Mendownload PDF`"
            )
            file_id = callbackQuery.message.reply_to_message.document.file_id
            fileSize = callbackQuery.message.reply_to_message.document.file_size
            # DOWNLOAD PROGRESS
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
            checked = await checkPdf(
                f'{callbackQuery.message.message_id}/pdf.pdf', callbackQuery
            )
            if not(checked == "pass"):
                await downloadMessage.delete()
                return
            doc = fitz.open(f'{callbackQuery.message.message_id}/pdf.pdf')
            number_of_pages = doc.pageCount
            if data in ["KIA", "KDA"]:
                pageStartAndEnd = [1, int(number_of_pages)]
            if data in ["KIR", "KDR"]:
                if not(int(pageStartAndEnd[1]) <= int(number_of_pages)):
                    await bot.edit_message_text(
                        chat_id = callbackQuery.message.chat.id,
                        message_id = downloadMessage.message_id,
                        text = f"`PDF hanya mempunyai {number_of_pages} pages`"
                    )
                    PROCESS.remove(callbackQuery.message.chat.id)
                    shutil.rmtree(f"{callbackQuery.message.message_id}")
                    return
            zoom = 2
            mat = fitz.Matrix(zoom, zoom)
            if data in ["KIA", "KDA", "KIR", "KDR"]:
                if int(int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])) >= 11:
                    await bot.pin_chat_message(
                        chat_id = callbackQuery.message.chat.id,
                        message_id = downloadMessage.message_id,
                        disable_notification = True,
                        both_sides = True
                    )
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = downloadMessage.message_id,
                    text = f"`📄 - Total halaman: {int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])}`"
                )
                totalPgList = range(int(pageStartAndEnd[0]), int(pageStartAndEnd[1])+1)
                cnvrtpg = 0
                for i in range(0, len(totalPgList), 10):
                    pgList = totalPgList[i:i+10]
                    os.mkdir(f'{callbackQuery.message.message_id}/pgs')
                    for pageNo in pgList:
                        page = doc.loadPage(pageNo-1)
                        pix = page.getPixmap(matrix = mat)
                        cnvrtpg += 1
                        if cnvrtpg % 5 == 0:
                            await bot.edit_message_text(
                                chat_id = callbackQuery.message.chat.id,
                                message_id = downloadMessage.message_id,
                                text = f"`Converted: {cnvrtpg}/{int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])} pages.. 🤞`"
                            )
                        if callbackQuery.message.chat.id not in PROCESS:
                            try:
                                await bot.edit_message_text(
                                    chat_id = callbackQuery.message.chat.id,
                                    message_id = downloadMessage.message_id,
                                    text = f"`Dibatalkan pada {cnvrtpg}/{int(int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0]))} pages.. 🙄`"
                                )
                                shutil.rmtree(f'{callbackQuery.message.message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        with open(
                            f'{callbackQuery.message.message_id}/pgs/{pageNo}.jpg','wb'
                        ):
                            pix.writePNG(f'{callbackQuery.message.message_id}/pgs/{pageNo}.jpg')
                    try:
                        await bot.edit_message_text(
                            chat_id = callbackQuery.message.chat.id,
                            message_id = downloadMessage.message_id,
                            text = f"`⏳ - Menyiapkan gambar` 🤹"
                        )
                    except Exception:
                        pass
                    directory = f'{callbackQuery.message.message_id}/pgs'
                    imag = [os.path.join(directory, file) for file in os.listdir(directory)]
                    imag.sort(key=os.path.getctime)
                    media[callbackQuery.message.chat.id] = []
                    mediaDoc[callbackQuery.message.chat.id] = []
                    LrgFileNo = 1
                    for file in imag:
                        if os.path.getsize(file) >= 1000000:
                            picture = Image.open(file)
                            CmpImg = f'{callbackQuery.message.message_id}/pgs/temp{LrgFileNo}.jpeg'
                            picture.save(
                                CmpImg,
                                "JPEG",
                                optimize=True,
                                quality = 75
                            )
                            LrgFileNo += 1
                            file = CmpImg
                            if os.path.getsize(CmpImg) >= 1000000:
                                picture = Image.open(CmpImg)
                                CmpCmpImg = f'{callbackQuery.message.message_id}/pgs/temP{LrgFileNo}.jpeg'
                                picture.save(
                                    CmpCmpImg,
                                    "JPEG",
                                    optimize=True,
                                    quality=75
                                )
                                file = CmpCmpImg
                                if os.path.getsize(CmpCmpImg) >= 1000000:
                                    picture = Image.open(CmpCmpImg)
                                    CmpCmpCmpImg = f'{callbackQuery.message.message_id}/pgs/teMP{LrgFileNo}.jpeg'
                                    picture.save(
                                        CmpCmpCmpImg,
                                        "JPEG",
                                        optimize=True,
                                        quality=75
                                    )
                                    file = CmpCmpCmpImg
                                    if os.path.getsize(CmpCmpImg) >= 1000000:
                                        continue
                                    else:
                                        media[
                                            callbackQuery.message.chat.id
                                        ].append(
                                            InputMediaPhoto(media = file)
                                        )
                                        mediaDoc[
                                            callbackQuery.message.chat.id
                                        ].append(
                                            InputMediaDocument(media = file)
                                        )
                                        continue
                                else:
                                    media[
                                        callbackQuery.message.chat.id
                                    ].append(
                                        InputMediaPhoto(media = file)
                                    )
                                    mediaDoc[
                                        callbackQuery.message.chat.id
                                    ].append(
                                        InputMediaDocument(media = file)
                                    )
                                    continue
                            else:
                                media[
                                    callbackQuery.message.chat.id
                                ].append(
                                    InputMediaPhoto(media = file)
                                )
                                mediaDoc[
                                    callbackQuery.message.chat.id
                                ].append(
                                    InputMediaDocument(media = file)
                                )
                                continue
                        media[
                            callbackQuery.message.chat.id
                        ].append(
                            InputMediaPhoto(media = file)
                        )
                        mediaDoc[
                            callbackQuery.message.chat.id
                        ].append(
                            InputMediaDocument(media = file)
                        )
                    await bot.edit_message_text(
                        chat_id = callbackQuery.message.chat.id,
                        message_id = downloadMessage.message_id,
                        text = f"`Mengupload: {cnvrtpg}/{int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])} halaman..`"
                    )
                    if data in ["KIA", "KIR"]:
                        if callbackQuery.message.chat.id not in PROCESS:
                            try:
                                shutil.rmtree(f'{callbackQuery.message.message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        await bot.send_chat_action(
                            callbackQuery.message.chat.id, "upload_photo"
                        )
                        try:
                            await bot.send_media_group(
                                callbackQuery.message.chat.id,
                                media[callbackQuery.message.chat.id]
                            )
                        except Exception:
                            del media[callbackQuery.message.chat.id]
                            del mediaDoc[callbackQuery.message.chat.id]
                    if data in ["KDA", "KDR"]:
                        if callbackQuery.message.chat.id not in PROCESS:
                            try:
                                shutil.rmtree(f'{callbackQuery.message.message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        await bot.send_chat_action(
                            callbackQuery.message.chat.id, "upload_document"
                        )
                        try:
                            await bot.send_media_group(
                                callbackQuery.message.chat.id,
                                mediaDoc[callbackQuery.message.chat.id]
                            )
                        except Exception:
                            del mediaDoc[callbackQuery.message.chat.id]
                            del media[callbackQuery.message.chat.id]
                    shutil.rmtree(f'{callbackQuery.message.message_id}/pgs')
                PROCESS.remove(callbackQuery.message.chat.id)
                doc.close()
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = downloadMessage.message_id,
                    text = f'`✅ - Berhasil mengupload `🏌️'
                )
                shutil.rmtree(f'{callbackQuery.message.message_id}')
            if data in ["KIS", "KDS"]:
                if int(len(newList)) >= 11:
                    await bot.pin_chat_message(
                        chat_id = callbackQuery.message.chat.id,
                        message_id = downloadMessage.message_id,
                        disable_notification = True,
                        both_sides = True
                    )
                totalPgList = []
                for i in newList:
                    if 1 <= int(i) <= number_of_pages:
                        totalPgList.append(i)
                if len(totalPgList) < 1:
                    await bot.edit_message_text(
                        chat_id = callbackQuery.message.chat.id,
                        message_id = downloadMessage.message_id,
                        text = f"`PDF hanya mempunyai {number_of_pages} halaman`"
                    )
                    PROCESS.remove(callbackQuery.message.chat.id)
                    shutil.rmtree(f'{callbackQuery.message.message_id}')
                    doc.close()
                    return
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = downloadMessage.message_id,
                    text = f"`📄 - Total halaman: {len(totalPgList)}`"
                )
                cnvrtpg = 0
                for i in range(0, len(totalPgList), 10):
                    pgList = totalPgList[i:i+10]
                    os.mkdir(f'{callbackQuery.message.message_id}/pgs')
                    for pageNo in pgList:
                        if int(pageNo) <= int(number_of_pages):
                            page = doc.loadPage(int(pageNo)-1)
                            pix = page.getPixmap(matrix = mat)
                        else:
                            continue
                        cnvrtpg += 1
                        if cnvrtpg % 5 == 0:
                            await bot.edit_message_text(
                                chat_id = callbackQuery.message.chat.id,
                                message_id = downloadMessage.message_id,
                                text = f"`Converted: {cnvrtpg}/{len(totalPgList)} halaman..`"
                            )
                        if callbackQuery.message.chat.id not in PROCESS:
                            try:
                                await bot.edit_message_text(
                                    chat_id = callbackQuery.message.chat.id,
                                    message_id = downloadMessage.message_id,
                                    text = f"`Dibatalkan pada {cnvrtpg}/{len(totalPgList)} halaman..`"
                                )
                                shutil.rmtree(f'{callbackQuery.message.message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        with open(
                            f'{callbackQuery.message.message_id}/pgs/{pageNo}.jpg','wb'
                        ):
                            pix.writePNG(f'{callbackQuery.message.message_id}/pgs/{pageNo}.jpg')
                    try:
                        await bot.edit_message_text(
                            chat_id = callbackQuery.message.chat.id,
                            message_id = downloadMessage.message_id,
                            text = f"`⏳ - Menyiapkan gambar`"
                        )
                    except Exception:
                        pass
                    directory = f'{callbackQuery.message.message_id}/pgs'
                    imag = [os.path.join(directory, file) for file in os.listdir(directory)]
                    imag.sort(key=os.path.getctime)
                    media[callbackQuery.message.chat.id] = []
                    mediaDoc[callbackQuery.message.chat.id] = []
                    LrgFileNo = 1
                    for file in imag:
                        if os.path.getsize(file) >= 1000000:
                            picture = Image.open(file)
                            CmpImg = f'{callbackQuery.message.message_id}/pgs/temp{LrgFileNo}.jpeg'
                            picture.save(
                                CmpImg,
                                "JPEG",
                                optimize=True,
                                quality = 75
                            ) 
                            LrgFileNo += 1
                            file = CmpImg
                            if os.path.getsize(CmpImg) >= 1000000:
                                picture = Image.open(CmpImg)
                                CmpCmpImg = f'{callbackQuery.message.message_id}/pgs/temP{LrgFileNo}.jpeg'
                                picture.save(
                                    CmpCmpImg,
                                    "JPEG",
                                    optimize=True,
                                    quality=75
                                )
                                file = CmpCmpImg
                                if os.path.getsize(CmpCmpImg) >= 1000000:
                                    picture = Image.open(CmpCmpImg)
                                    CmpCmpCmpImg = f'{callbackQuery.message.message_id}/pgs/teMP{LrgFileNo}.jpeg'
                                    picture.save(
                                        CmpCmpCmpImg,
                                        "JPEG",
                                        optimize=True,
                                        quality=75
                                    )
                                    file = CmpCmpCmpImg
                                    if os.path.getsize(CmpCmpImg) >= 1000000:
                                        continue
                                    else:
                                        media[
                                            callbackQuery.message.chat.id
                                        ].append(
                                            InputMediaPhoto(media = file)
                                        )
                                        mediaDoc[
                                            callbackQuery.message.chat.id
                                        ].append(
                                            InputMediaDocument(media = file)
                                        )
                                        continue
                                else:
                                    media[
                                        callbackQuery.message.chat.id
                                    ].append(
                                        InputMediaPhoto(media = file)
                                    )
                                    mediaDoc[
                                        callbackQuery.message.chat.id
                                    ].append(
                                        InputMediaDocument(media = file)
                                    )
                                    continue
                            else:
                                media[
                                    callbackQuery.message.chat.id
                                ].append(
                                    InputMediaPhoto(media = file)
                                )
                                mediaDoc[
                                    callbackQuery.message.chat.id
                                ].append(
                                    InputMediaDocument(media = file)
                                )
                                continue
                        media[
                            callbackQuery.message.chat.id
                        ].append(
                            InputMediaPhoto(media = file)
                        )
                        mediaDoc[
                            callbackQuery.message.chat.id
                        ].append(
                            InputMediaDocument(media = file)
                        )
                    await bot.edit_message_text(
                        chat_id = callbackQuery.message.chat.id,
                        message_id = downloadMessage.message_id,
                        text = f"`Mengupload: {cnvrtpg}/{len(totalPgList)} halaman..`"
                    )
                    if data == "KIS":
                        if callbackQuery.message.chat.id not in PROCESS:
                            try:
                                shutil.rmtree(f'{callbackQuery.message.message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        await bot.send_chat_action(
                            callbackQuery.message.chat.id, "upload_photo"
                        )
                        try:
                            await bot.send_media_group(
                                callbackQuery.message.chat.id,
                                media[callbackQuery.message.chat.id]
                            )
                        except Exception:
                            del media[callbackQuery.message.chat.id]
                            del mediaDoc[callbackQuery.message.chat.id]
                    if data == "KDS":
                        if callbackQuery.message.chat.id not in PROCESS:
                            try:
                                shutil.rmtree(f'{callbackQuery.message.message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        await bot.send_chat_action(
                            callbackQuery.message.chat.id, "upload_document"
                        )
                        try:
                            await bot.send_media_group(
                                callbackQuery.message.chat.id,
                                mediaDoc[callbackQuery.message.chat.id]
                            )
                        except Exception:
                            del mediaDoc[callbackQuery.message.chat.id]
                            del media[callbackQuery.message.chat.id]
                    shutil.rmtree(f'{callbackQuery.message.message_id}/pgs')
                PROCESS.remove(callbackQuery.message.chat.id)
                doc.close()
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = downloadMessage.message_id,
                    text = f'`✅ - Berhasil mengupload `🏌️'
                )
                shutil.rmtree(f'{callbackQuery.message.message_id}')
    except Exception as e:
        try:
            print("image: ", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f'{callbackQuery.message.message_id}')
        except Exception:
            pass


# Copyright InHame Dev
