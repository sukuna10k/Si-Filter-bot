import random

import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

@Client.on_message(filters.command(["wall", "wallpaper"]))
async def wall(_, message: Message):
    " ғɪxᴇᴅ ᴡᴀʟʟ ʙʏ ᴍɪᴋᴇʏ"
    try:
        text = message.text.split(None, 1)[1]
    except IndexError:
        text = None
    if not text:
        return await message.reply_text("`Veuillez fournir une requête pour la recherche.`")
    m = await message.reply_text("`Recherche de fonds d'écran...`")
    try:
        url = requests.get(f"https://api.safone.me/wall?query={text}").json()["results"]
        ran = random.randint(0, 3)
        await message.reply_photo(
            photo=url[ran]["imageUrl"],
            caption=f"🥀 **Requêté par :** {message.from_user.mention}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Lien", url=url[ran]["imageUrl"])],
                ]
            ),
        )
        await m.delete()
    except Exception as e:
        await m.edit_text(
            f"`Fond d'écran non trouvé pour : `{text}`",
        )
