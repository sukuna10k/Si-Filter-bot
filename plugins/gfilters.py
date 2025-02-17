import io
from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.gfilters_mdb import(
   add_gfilter,
   get_gfilters,
   delete_gfilter,
   count_gfilters
)

from database.connections_mdb import active_connection
from utils import get_file_id, gfilterparser, split_quotes
from info import ADMINS


@Client.on_message(filters.command(['gfilter', 'addg']) & filters.incoming & filters.user(ADMINS))
async def addgfilter(client, message):
    args = message.text.html.split(None, 1)

    if len(args) < 2:
        await message.reply_text("Commande incomplète :(", quote=True)
        return

    extracted = split_quotes(args[1])
    text = extracted[0].lower()

    if not message.reply_to_message and len(extracted) < 2:
        await message.reply_text("Ajoutez du contenu pour enregistrer votre filtre !", quote=True)
        return

    if (len(extracted) >= 2) and not message.reply_to_message:
        reply_text, btn, alert = gfilterparser(extracted[1], text)
        fileid = None
        if not reply_text:
            await message.reply_text("Vous ne pouvez pas avoir de boutons seuls, ajoutez du texte pour les accompagner !", quote=True)
            return

    elif message.reply_to_message and message.reply_to_message.reply_markup:
        try:
            rm = message.reply_to_message.reply_markup
            btn = rm.inline_keyboard
            msg = get_file_id(message.reply_to_message)
            if msg:
                fileid = msg.file_id
                reply_text = message.reply_to_message.caption.html
            else:
                reply_text = message.reply_to_message.text.html
                fileid = None
            alert = None
        except:
            reply_text = ""
            btn = "[]" 
            fileid = None
            alert = None

    elif message.reply_to_message and message.reply_to_message.media:
        try:
            msg = get_file_id(message.reply_to_message)
            fileid = msg.file_id if msg else None
            reply_text, btn, alert = gfilterparser(extracted[1], text) if message.reply_to_message.sticker else gfilterparser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.text:
        try:
            fileid = None
            reply_text, btn, alert = gfilterparser(message.reply_to_message.text.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    else:
        return

    await add_gfilter('gfilters', text, reply_text, btn, fileid, alert)

    await message.reply_text(
        f"GFilter pour  `{text}`  ajouté",
        quote=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )


@Client.on_message(filters.command(['viewgfilters', 'gfilters']) & filters.incoming & filters.user(ADMINS))
async def get_all_gfilters(client, message):
    texts = await get_gfilters('gfilters')
    count = await count_gfilters('gfilters')
    if count:
        gfilterlist = f"Nombre total de gfilters : {count}\n\n"

        for text in texts:
            keywords = " ×  `{}`\n".format(text)

            gfilterlist += keywords

        if len(gfilterlist) > 4096:
            with io.BytesIO(str.encode(gfilterlist.replace("`", ""))) as keyword_file:
                keyword_file.name = "keywords.txt"
                await message.reply_document(
                    document=keyword_file,
                    quote=True
                )
            return
    else:
        gfilterlist = f"Aucun gfilter actif."

    await message.reply_text(
        text=gfilterlist,
        quote=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )
        
@Client.on_message(filters.command('delg') & filters.incoming & filters.user(ADMINS))
async def deletegfilter(client, message):
    try:
        cmd, text = message.text.split(" ", 1)
    except:
        await message.reply_text(
            "<i>Indiquez le nom du gfilter que vous souhaitez supprimer !</i>\n\n"
            "<code>/delg nom_du_gfilter</code>\n\n"
            "Utilisez /viewgfilters pour voir tous les gfilters disponibles",
            quote=True
        )
        return

    query = text.lower()

    await delete_gfilter(message, query, 'gfilters')

@Client.on_message(filters.command('delallg') & filters.user(ADMINS))
async def delallgfilters(client, message):
    await message.reply_text(
            f"Voulez-vous vraiment continuer ?",
            reply_markup=InlineKeyboardMarkup([ 
                [InlineKeyboardButton(text="OUI", callback_data="gfiltersdeleteallconfirm")],
                [InlineKeyboardButton(text="ANNULER", callback_data="gfiltersdeleteallcancel")]
            ]),
            quote=True
        )
