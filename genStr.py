import asyncio

from bot import bot, HU_APP
from pyromod import listen
from asyncio.exceptions import TimeoutError
from genTele import telethon

from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired
)

START_TEXT = """Hi, {}.
Mau cari strings ya ngab walah paskali kamu datang ke sini ngab\n
Oleh @kenkanasw"""


API_TEXT = "Hi, {}. Kirim api nya ngab `API_ID` yang sama dengan `APP_ID` untuk dapatkan string ngab."
HASH_TEXT = "Sekarang kirim `API_HASH`.\n\n klik /cancel Untuk membatalkan tugas."
PHONE_NUMBER_TEXT = (
    "Sekarang kirim no telegram mu ngab dengan format internasional.\n"
    "Termasuk kode negara ngab. Contoh: **+14154566376**\n\n"
    "Klik /cancel Untuk membatalkan tugas."
)

@bot.on_message(filters.private & filters.command ("start"))
async def genStr(_, msg: Message):
    chat = msg.chat
    text = await bot.ask(
        chat.id, START_TEXT.format(msg.from_user.mention)
    )
@bot.on_message(filters.private & filters.command ("pyrogram"))
async def genStr(_, msg: Message):
    chat = msg.chat
    api = await bot.ask(
        chat.id, API_TEXT,format(msg.from_user.mention)
     )
@bot.on_message(filters.private & filters.command ("telethon"))
async def genTele(_, msg: Message):
    chat = msg.chat
    
    if await is_cancel(msg, api.text):
        return
    try:
        check_api = int(api.text)
    except Exception:
        await msg.reply("`API_ID` Salah ngab.\nTekan /start Ulagi ngab.")
        return
    api_id = api.text
    hash = await bot.ask(chat.id, HASH_TEXT)
    if await is_cancel(msg, hash.text):
        return
    if not len(hash.text) >= 30:
        await msg.reply("`API_HASH` Salah ngab.\nKlik /start to Coba lagi ngab.")
        return
    api_hash = hash.text
    while True:
        number = await bot.ask(chat.id, PHONE_NUMBER_TEXT)
        if not number.text:
            continue
        if await is_cancel(msg, number.text):
            return
        phone = number.text
        confirm = await bot.ask(chat.id, f'`yakin "{phone}" sudah benar? (y/n):` \n\nKetik: `y` (untuk ya)\nKetik: `n` (untuk No)')
        if await is_cancel(msg, confirm.text):
            return
        if "y" in confirm.text:
            break
    try:
        client = Client("my_account", api_id=api_id, api_hash=api_hash)
    except Exception as e:
        await bot.send_message(chat.id ,f"**ERROR:** `{str(e)}`\nKetik /start Ulangi ngab.")
        return
    try:
        await client.connect()
    except ConnectionError:
        await client.disconnect()
        await client.connect()
    try:
        code = await client.send_code(phone)
        await asyncio.sleep(1)
    except FloodWait as e:
        await msg.reply(f"Sabar ngab terlalu banyak mencoba tunggu {e.x} detik")
        return
    except ApiIdInvalid:
        await msg.reply("API ID and API Hash Tidak ada.\n\nKlik /start Coba lagi ngab.")
        return
    except PhoneNumberInvalid:
        await msg.reply("Nomormu fake ngab.\n\nKlik /start Coba lagi ngab.")
        return
    try:
        otp = await bot.ask(
            chat.id, ("Kode OTP Sudah di kirim ke nomermu ngab, "
                      "Masukin ngab OTP dengan format `1 2 3 4 5` format. __(Kasih jarak 1 spaci ngab!)__ \n\n"
                      "If Bot tidak mengirim OTP Coba lagi ngab /restart dan start lagi ngab /start command ke bot.\n"
                      "Tekan /cancel untuk berhenti ngab."), timeout=300)

    except TimeoutError:
        await msg.reply("Dahlah waktu habis ngab sudah 5 min.\nTekan /start Coba lagi ngab.")
        return
    if await is_cancel(msg, otp.text):
        return
    otp_code = otp.text
    try:
        await client.sign_in(phone, code.phone_code_hash, phone_code=' '.join(str(otp_code)))
    except PhoneCodeInvalid:
        await msg.reply("Kode salah cuk.\n\nKlik /start Coba lagi ngab.")
        return
    except PhoneCodeExpired:
        await msg.reply("Kode kadaluarsa.\n\nKlik /start Coba lagi ngab.")
        return
    except SessionPasswordNeeded:
        try:
            two_step_code = await bot.ask(
                chat.id, 
                "Bajingan sesi dua langkah cuk.\nKirim Password loe cok.\n\nKlik /cancel Untuk berhenti dan putus.",
                timeout=300
            )
        except TimeoutError:
            await msg.reply("`Waktu sudah melebihi batas cuk 5 min.\n\nKlik /start Coba lagi ngab.`")
            return
        if await is_cancel(msg, two_step_code.text):
            return
        new_code = two_step_code.text
        try:
            await client.check_password(new_code)
        except Exception as e:
            await msg.reply(f"**ERROR:** `{str(e)}`")
            return
    except Exception as e:
        await bot.send_message(chat.id ,f"**ERROR:** `{str(e)}`")
        return
    try:
        session_string = await client.export_session_string()
        await client.send_message("me", f"#PYROGRAM #STRING_SESSION\n\n```{session_string}``` \n\nBy [@stringdurhakabot](tg://openmessage?user_id=1884857088) \nOwner bot @kenkanasw")
        await client.disconnect()
        text = "String sukses su di buat.\nKlik button su."
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Lihat String Session", url=f"tg://openmessage?user_id={chat.id}")]]
        )
        await bot.send_message(chat.id, text, reply_markup=reply_markup)
    except Exception as e:
        await bot.send_message(chat.id ,f"**ERROR:** `{str(e)}`")
        return


@bot.on_message(filters.private & filters.command("restart"))
async def restart(_, msg: Message):
    await msg.reply("Mulai ulang ngab!")
    HU_APP.restart()


@bot.on_message(filters.private & filters.command("help"))
async def restart(_, msg: Message):
    out = f"""
Hi, {msg.from_user.mention}. Ini Bot pembuat string ngab. \
Sini gue kasih `STRING_SESSION` Buat UserBot loe.

Gue minat `API_ID`, `API_HASH`, Nomer hp buat verifikasi kode. \
Yang di kirim ke telegram loe.
Loe dapat kirim **OTP** dengan `1 2 3 4 5` untuk format. __(Kasih jarak 1 spaci!)__

**NOTE:** Jika bot tidak mengirim kode OTP ke telegram loe coba klik /restart lalu coba lagi terus /start untuk mulai lagi ngab. 

Lu kalau mau tau Bot Updates join channel cuk !!
"""
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Channel', url='https://t.me/levinachannel'),
                InlineKeyboardButton('Developer', url='https://t.me/kenkanasw')
            ],
            [
                InlineKeyboardButton('Bots Updates Group', url='https://t.me/gcsupportbots'),
                InlineKeyboardButton('Github', url='https://github.com/jokokendi/Strings')
            ],
        ]
    )
    await msg.reply(out, reply_markup=reply_markup)


async def is_cancel(msg: Message, text: str):
    if text.startswith("/cancel"):
        await msg.reply("Proses di batalkan.")
        return True
    return False

if __name__ == "__main__":
    bot.run()
