import os
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyromod import listen
from burn import burning

load_dotenv()

Bot = Client(
    "Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_TXT = """
Hi {}, I'm Subtitle Muxer Bot.

Send a video to start.
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Source Code', url='https://github.com/soebb'),
        ]]
    )


@Bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TXT.format(update.from_user.mention)
    reply_markup = START_BTN
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


@Bot.on_message(filters.private & filters.media)
async def mux(bot, m):
    if m.document and not m.document.mime_type.startswith("video/"):
        return
    msg = await m.reply("Downloading video..")
    media = await m.download()
    ask_srt = await bot.ask(m.chat.id,'`Send the srt file`', filters=filters.document)
    await msg.edit_text("Processing..")
    srt = await bot.download_media(message=ask_srt.document)
    output_name = "muxed_" + os.path.basename(media)
    burning(media, srt, output_name)
    await m.reply_document(output_name)
    await msg.delete()
    os.remove(media)
    os.remove(srt)
    os.remove(output_name)


Bot.run()
