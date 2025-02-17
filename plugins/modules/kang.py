import os
import math
import urllib.request as urllib
import logging
from io import BytesIO
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import Message
from telegram.error import TelegramError
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def getConfig(name: str):
    return os.environ.get(name)

try:
    BOT_TOKEN = getConfig('BOT_TOKEN')
    API_ID = getConfig('API_ID')
    API_HASH = getConfig('API_HASH')
except KeyError as e:
    logger.error("Environment variables missing! Exiting now")
    exit(1)

bot = Client("Stickerbot", bot_token="7703758993:AAFGlr-avSP-LWUbiMRm4KBOaOdhanAEfHE", api_id=API_ID, api_hash=API_HASH)

@bot.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    start_text = (f"Hey! I'm {client.me.first_name}, and I'm a bot which allows you to create a sticker pack "
                  "from other stickers, images, and documents!")
    await message.reply_text(start_text)

@bot.on_message(filters.command("kang"))
async def kang_handler(client, message: Message):
    user = message.from_user
    msg = message.reply_to_message
    packnum = 0
    packname = f"a{user.id}_by_{client.me.username}"
    packname_found = False
    max_stickers = 120

    while not packname_found:
        try:
            stickerset = await client.get_sticker_set(packname)
            if len(stickerset.stickers) >= max_stickers:
                packnum += 1
                packname = f"a{packnum}_{user.id}_by_{client.me.username}"
            else:
                packname_found = True
        except TelegramError as e:
            if "Stickerset_invalid" in str(e):
                packname_found = True

    if msg and (msg.sticker or msg.photo or msg.document):
        file_id = msg.sticker.file_id if msg.sticker else msg.photo[-1].file_id if msg.photo else msg.document.file_id
        file = await client.download_media(file_id, file_name='kangsticker.png')

        sticker_emoji = "🤔"  # Default emoji
        if msg.sticker and msg.sticker.emoji:
            sticker_emoji = msg.sticker.emoji
        
        im = Image.open(file)
        max_size = (512, 512)
        im.thumbnail(max_size)
        im.save(file, "PNG")

        try:
            await client.add_sticker_to_set(user.id, packname, png_sticker=open(file, 'rb'), emojis=sticker_emoji)
            await message.reply_text(f"Sticker added to [pack](t.me/addstickers/{packname}) with emoji {sticker_emoji}", parse_mode="markdown")
        except TelegramError as e:
            await message.reply_text(f"Failed to add sticker: {str(e)}")
    else:
        await message.reply_text("Please reply to a sticker, photo, or document to kang it!")

    if os.path.exists("kangsticker.png"):
        os.remove("kangsticker.png")

if __name__ == "__main__":
    bot.run()
