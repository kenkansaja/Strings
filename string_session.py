#!/usr/bin/env python3
# (c) https://t.me/TelethonChat/37677 and SpEcHiDe
#


from telethon.sync import TelegramClient
from telethon.sessions import StringSession

@bot.on_message(filters.private & filters.command ("teleton"))
async def string_session(_, msg: Message):
print("""Silakan masuk ke my.telegram.org atau @Kenkanrobot
Masuk menggunakan akun Telegram Anda
Klik pada Alat Pengembangan API
Buat aplikasi baru, dengan memasukkan detail yang diperlukan
Periksa bagian pesan tersimpan Telegram Anda untuk menyalin STRING_SESSION""")
API_KEY = int(input("Enter API_KEY here: "))
API_HASH = input("Enter API_HASH here: ")

with TelegramClient(StringSession(), API_KEY, API_HASH) as client:
    print("Check Telegram Save Message Mu Untuk Copy STRING_SESSION ")
    session_string = client.session.save()
    saved_messages_template = """Grup Support @musikkugroup

<code>STRING_SESSION</code>: <code>{}</code>

⚠️ <i>Harap berhati-hati sebelum memberikan nilai ini ke pihak ketiga</i>""".format(session_string)
    client.send_message("me", saved_messages_template, parse_mode="html")
