from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from info import *
from urllib.parse import quote_plus
from util.file_properties import get_name, get_hash, get_media_file_size
from util.human_readable import humanbytes
import humanize
import asyncio
import random

"""ajouter le temps en secondes avant la suppression
1min=60, 2min=60×2=120, 5min=60×5=300"""
SECONDS = int(os.getenv("SECONDS", "10"))

@Client.on_message(filters.private & filters.command("stream"))
async def stream_start(client, message):
    if STREAM_MODE == False:
        return 
    msg = await client.ask(message.chat.id, "**Maintenant, envoie-moi ton fichier/vidéo pour obtenir un lien de streaming et de téléchargement rapide**")
    if not msg.media:
        return await message.reply("**S'il te plaît, envoie-moi un média supporté.**")
    if msg.media in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
        file = getattr(msg, msg.media.value)
        filename = file.file_name
        filesize = humanize.naturalsize(file.file_size) 
        fileid = file.file_id
        user_id = message.from_user.id
        username =  message.from_user.mention 

        log_msg = await client.send_cached_media(
            chat_id=LOG_CHANNEL,
            file_id=fileid,
        )
        fileName = {quote_plus(get_name(log_msg))}
        lazy_stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        lazy_download = f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
 
        await log_msg.reply_text(
            text=f"•• Lien généré pour l'ID #{user_id} \n•• Nom d'utilisateur : {username} \n\n•• Nom du fichier : {fileName}",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("• Télécharger", url=lazy_download),  # lien de téléchargement
                                                InlineKeyboardButton('Regarder •', url=lazy_stream)]])  # lien de streaming
        )
        rm=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("• Regarder", url=lazy_stream),
                    InlineKeyboardButton('Télécharger •', url=lazy_download)
                ]
            ] 
        )
        msg_text = """<i><u>Voici ton lien généré !</u></i>\n\n<b>📂 Nom du fichier :</b> <i>{}</i>\n\n<b>📦 Taille du fichier :</b> <i>{}</i>\n\n<b>📥 Télécharger :</b> <i>{}</i>\n\n<b> 🖥 Regarder :</b> <i>{}</i>\n\n<b>🚸 Remarque : le lien n'expirera pas tant que je ne le supprimerai pas</b>\n\nBaka! Le lien sera supprimé après 1 minute. Sauvegarde-le dans les messages sauvegardés maintenant!.</b>"""

        lazy_d = await message.reply_text(text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(msg)), lazy_download, lazy_stream), quote=True, disable_web_page_preview=True, reply_markup=rm)
        await asyncio.sleep(60)
        await lazy_d.delete()
