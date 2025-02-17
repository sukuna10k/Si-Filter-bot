import os
import math
import urllib.request as urllib
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import BadRequest

# Configuration du logging
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Message de démarrage
START_TEXT = """
Hey ! Je suis {}, un bot qui te permet de créer un pack de stickers à partir d'autres stickers, images et documents !
Je n'ai que quelques commandes, donc je n'ai pas de menu d'aide ou quelque chose comme ça.
Tu peux aussi consulter le code source du bot [ici](https://github.com/breakdowns/kang-stickerbot)
"""

# Gestionnaire de la commande /starts
@Client.on_message(filters.command("starts") & filters.private)
async def starts(client: Client, message: Message):
    await message.reply_text(
        START_TEXT.format((await client.get_me()).first_name),
        parse_mode="markdown"
    )

# Gestionnaire de la commande /kang
@Client.on_message(filters.command("kang"))
async def kang(client: Client, message: Message):
    user = message.from_user
    packnum = 0
    packname = f"a{user.id}_by_{client.me.username}"
    packname_found = 0
    max_stickers = 120

    while packname_found == 0:
        try:
            stickerset = await client.get_sticker_set(packname)
            if len(stickerset.stickers) >= max_stickers:
                packnum += 1
                packname = f"a{packnum}_{user.id}_by_{client.me.username}"
            else:
                packname_found = 1
        except BadRequest as e:
            if "Stickerset_invalid" in str(e):
                packname_found = 1

    if message.reply_to_message:
        if message.reply_to_message.sticker:
            file_id = message.reply_to_message.sticker.file_id
        elif message.reply_to_message.photo:
            file_id = message.reply_to_message.photo.file_id
        elif message.reply_to_message.document:
            file_id = message.reply_to_message.document.file_id
        else:
            await message.reply_text("Ouais, je ne peux pas kang ça.")
            return

        kang_file = await client.download_media(file_id, file_name="kangsticker.png")

        if len(message.command) > 1:
            sticker_emoji = message.command[1]
        elif message.reply_to_message.sticker and message.reply_to_message.sticker.emoji:
            sticker_emoji = message.reply_to_message.sticker.emoji
        else:
            sticker_emoji = "🤔"

        try:
            im = Image.open(kang_file)
            if (im.width and im.height) < 512:
                size1 = im.width
                size2 = im.height
                if im.width > im.height:
                    scale = 512 / size1
                    size1new = 512
                    size2new = size2 * scale
                else:
                    scale = 512 / size2
                    size1new = size1 * scale
                    size2new = 512
                size1new = math.floor(size1new)
                size2new = math.floor(size2new)
                sizenew = (size1new, size2new)
                im = im.resize(sizenew)
            else:
                maxsize = (512, 512)
                im.thumbnail(maxsize)

            if not message.reply_to_message.sticker:
                im.save(kang_file, "PNG")

            await client.add_sticker_to_set(
                user_id=user.id,
                name=packname,
                png_sticker=kang_file,
                emojis=sticker_emoji
            )
            await message.reply_text(
                f"Sticker ajouté avec succès au [pack](t.me/addstickers/{packname})"
                f"\nL'emoji est : {sticker_emoji}",
                parse_mode="markdown"
            )
        except OSError as e:
            await message.reply_text("Je ne peux kang que des images, mec.")
            logger.error(e)
            return
        except BadRequest as e:
            if "Internal Server Error: sticker set not found (500)" in str(e):
                await message.reply_text(
                    f"Sticker ajouté avec succès au [pack](t.me/addstickers/{packname})"
                    f"\nL'emoji est : {sticker_emoji}",
                    parse_mode="markdown"
                )
            elif "Invalid sticker emojis" in str(e):
                await message.reply_text("Emoji(s) invalide(s).")
            elif "Sticker_png_dimensions" in str(e):
                im.save(kang_file, "PNG")
                await client.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    png_sticker=kang_file,
                    emojis=sticker_emoji
                )
                await message.reply_text(
                    f"Sticker ajouté avec succès au [pack](t.me/addstickers/{packname})"
                    f"\nL'emoji est : {sticker_emoji}",
                    parse_mode="markdown"
                )
            elif "Stickers_too_much" in str(e):
                await message.reply_text("Taille maximale du pack atteinte. Appuyez sur F pour payer le respect.")
            elif "Stickerset_invalid" in str(e):
                await makepack_internal(client, message, kang_file, sticker_emoji, packname, packnum)
            logger.error(e)
    else:
        packs = "Réponds à un sticker ou à une image pour le kang !\nOh, au fait, voici tes packs :\n"
        if packnum > 0:
            firstpackname = f"a{user.id}_by_{client.me.username}"
            for i in range(packnum + 1):
                if i == 0:
                    packs += f"[pack](t.me/addstickers/{firstpackname})\n"
                else:
                    packs += f"[pack{i}](t.me/addstickers/{packname})\n"
        else:
            packs += f"[pack](t.me/addstickers/{packname})"
        await message.reply_text(packs, parse_mode="markdown")

    if os.path.isfile(kang_file):
        os.remove(kang_file)

# Gestionnaire de la commande /kangurl
@Client.on_message(filters.command("kangurl"))
async def kangurl(client: Client, message: Message):
    user = message.from_user
    packnum = 0
    packname = f"a{user.id}_by_{client.me.username}"
    packname_found = 0
    max_stickers = 120

    while packname_found == 0:
        try:
            stickerset = await client.get_sticker_set(packname)
            if len(stickerset.stickers) >= max_stickers:
                packnum += 1
                packname = f"a{packnum}_{user.id}_by_{client.me.username}"
            else:
                packname_found = 1
        except BadRequest as e:
            if "Stickerset_invalid" in str(e):
                packname_found = 1

    if len(message.command) > 1:
        try:
            urlemoji = message.text.split(" ")
            png_sticker = urlemoji[1]
            sticker_emoji = urlemoji[2] if len(urlemoji) > 2 else "🤔"
            urllib.urlretrieve(png_sticker, 'kangsticker.png')
            im = Image.open('kangsticker.png')

            if (im.width and im.height) < 512:
                size1 = im.width
                size2 = im.height
                if im.width > im.height:
                    scale = 512 / size1
                    size1new = 512
                    size2new = size2 * scale
                else:
                    scale = 512 / size2
                    size1new = size1 * scale
                    size2new = 512
                size1new = math.floor(size1new)
                size2new = math.floor(size2new)
                sizenew = (size1new, size2new)
                im = im.resize(sizenew)
            else:
                maxsize = (512, 512)
                im.thumbnail(maxsize)

            im.save('kangsticker.png', "PNG")
            await message.reply_photo(photo='kangsticker.png')
            await client.add_sticker_to_set(
                user_id=user.id,
                name=packname,
                png_sticker='kangsticker.png',
                emojis=sticker_emoji
            )
            await message.reply_text(
                f"Sticker ajouté avec succès au [pack](t.me/addstickers/{packname})"
                f"\nL'emoji est : {sticker_emoji}",
                parse_mode="markdown"
            )
        except OSError as e:
            await message.reply_text("Je ne peux kang que des images, mec.")
            logger.error(e)
            return
        except BadRequest as e:
            if "Internal Server Error: sticker set not found (500)" in str(e):
                await message.reply_text(
                    f"Sticker ajouté avec succès au [pack](t.me/addstickers/{packname})"
                    f"\nL'emoji est : {sticker_emoji}",
                    parse_mode="markdown"
                )
            elif "Invalid sticker emojis" in str(e):
                await message.reply_text("Emoji(s) invalide(s).")
            elif "Sticker_png_dimensions" in str(e):
                im.save('kangsticker.png', "PNG")
                await client.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    png_sticker='kangsticker.png',
                    emojis=sticker_emoji
                )
                await message.reply_text(
                    f"Sticker ajouté avec succès au [pack](t.me/addstickers/{packname})"
                    f"\nL'emoji est : {sticker_emoji}",
                    parse_mode="markdown"
                )
            elif "Stickers_too_much" in str(e):
                await message.reply_text("Taille maximale du pack atteinte. Appuyez sur F pour payer le respect.")
            elif "Stickerset_invalid" in str(e):
                await makepack_internal(client, message, 'kangsticker.png', sticker_emoji, packname, packnum)
            logger.error(e)
    else:
        packs = "Réponds à un sticker ou à une image pour le kang !\nOh, au fait, voici tes packs :\n"
        if packnum > 0:
            firstpackname = f"a{user.id}_by_{client.me.username}"
            for i in range(packnum + 1):
                if i == 0:
                    packs += f"[pack](t.me/addstickers/{firstpackname})\n"
                else:
                    packs += f"[pack{i}](t.me/addstickers/{packname})\n"
        else:
            packs += f"[pack](t.me/addstickers/{packname})"
        await message.reply_text(packs, parse_mode="markdown")

    if os.path.isfile("kangsticker.png"):
        os.remove("kangsticker.png")

# Fonction pour créer un nouveau pack de stickers
async def makepack_internal(client: Client, message: Message, png_sticker, emoji, packname, packnum):
    user = message.from_user
    name = user.first_name[:50]
    try:
        extra_version = f" {packnum}" if packnum > 0 else ""
        await client.create_new_sticker_set(
            user.id,
            packname,
            f"{name}s kang pack{extra_version}",
            png_sticker=png_sticker,
            emojis=emoji
        )
        await message.reply_text(
            f"Pack de stickers créé avec succès. Tu peux le trouver [ici](t.me/addstickers/{packname})",
            parse_mode="markdown"
        )
    except BadRequest as e:
        if "Internal Server Error: created sticker set not found (500)" in str(e):
            await message.reply_text(
                f"Pack de stickers créé avec succès. Tu peux le trouver [ici](t.me/addstickers/{packname})",
                parse_mode="markdown"
            )
        elif "Peer_id_invalid" in str(e):
            await message.reply_text(
                "Contacte-moi d'abord en MP.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                    text="Start", url=f"t.me/{client.me.username}")]])
            )
        elif "Sticker set name is already occupied" in str(e):
            await message.reply_text(
                f"Ton pack peut être trouvé [ici](t.me/addstickers/{packname})",
                parse_mode="markdown"
            )
        logger.error(e)