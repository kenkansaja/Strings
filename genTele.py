from pyrogram import filters
from pyrogram.types import CallbackQuery

from telethon import (
    TelegramClient,
    events,
    custom
)
from telethon.sessions import StringSession
from telethon.errors.rpcerrorlist import (
    SessionPasswordNeededError,
    PhoneCodeInvalidError
)

bot.on_message(filters.private & filters.command ("telethon"))
async def genStr(_, msg: Message):
    chat = msg.chat
    api_hash = await api_hash.text
            
async def teleCreateSession(api_id: int, api_hash: str):
    return TelegramClient(StringSession(), api_id=int(api_id), api_hash=str(api_hash))


@sessionCli.on_callback_query(filters.create(lambda _, __, query: 'sele_telethon' in query.data))
async def teleGen(sessionCli, callback_data):
    user_id = callback_data.from_user.id
    
    await sessionCli.delete_messages(
        user_id,
        callback_data.message.message_id
    )

    # Init the process to get `API_ID`
    API_ID = await sessionCli.ask(
        chat_id=user_id,
        text=(
            'Sini ngab `API_ID` nya .'
        )
    )
    if not (
        API_ID.text.isdigit()
    ):
        await sessionCli.send_message(
            chat_id=user_id,
            text='API_ID should be integer and valid in range limit.'
        )
        return
    
    # Init the process to get `API_HASH`
    API_HASH = await sessionCli.ask(
        chat_id=user_id,
        text=(
            'Sini ngab `API_HASH` nya.'
        )
    )
    
    # Init the prcess to get phone number.
    PHONE = await sessionCli.ask(
        chat_id=user_id,
        text=(
            'Sini ngab nomer hpnya format inter nasional contoh,`+1456826528` okey ngab'
        )
    )    
    
    try:
        userClient = await teleCreateSession(api_id=API_ID.text, api_hash=API_HASH.text)
    except Exception as e:
        await sessionCli.send_message(
            chat_id=user_id,
            text=(
                f'**Bego lu ngab ada yang salah cuk**:\n`{e}`'
            )
        )
    
    await userClient.connect()

    if str(PHONE.text).startswith('+'):
        sent_code = await userClient.send_code_request(PHONE.text)
        
        CODE = await sessionCli.ask(
                chat_id=user_id,
                text=(
                    'kirim kesini gab kodenya seperti ini ngab `1-2-3-4-5` bukan kayak gini `12345` awas ngab kalau salah.'
                )
            )
        try:
            await userClient.sign_in(PHONE.text, code=CODE.text.replace('-', ''), password=None)
        except PhoneCodeInvalidError:
            await sessionCli.send_message(
                chat_id=user_id,
                text=(
                    'Kodenya salah ngab coba lagi cuk /start'
                )
            )
            return
        except Exception as e:
            PASSWORD = await sessionCli.ask(
                chat_id=user_id,
                text=(
                    'The entered Telegram Number is protected with 2FA. Please enter your second factor authentication code.\n__This message will only be used for generating your string session, and will never be used for any other purposes than for which it is asked.__'
                )
            )
            await userClient.sign_in(password=PASSWORD.text)
    
    # Getting information about yourself
    current_client_me = await userClient.get_me()
    # "me" is an User object. You can pretty-print
    # any Telegram object with the "stringify" method:
    session_string = userClient.session.save()
    
    await sessionCli.send_message(
            chat_id=user_id,
            text=f"**Ini ngab Session String lu okey**: \n\n`{session_string}`"
            reply_markup = InlineKeyboardMarkup(
           [InlineKeyboardButton(text="Lihat String Session", url=f"tg://openmessage?user_id={chat.id}")]
           )     

    await sessionCli.send_message(
            chat_id=user_id,
            text=(
                f'{callback_data.from_user.mention} ( `{callback_data.from_user.id}` ) created new session.'
            )
        )    
