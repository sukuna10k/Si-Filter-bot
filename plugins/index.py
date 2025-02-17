import logging
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from info import ADMINS
from info import INDEX_REQ_CHANNEL as LOG_CHANNEL
from database.ia_filterdb import save_file
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import temp
import re
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lock = asyncio.Lock()

# Fonction de gestion des requêtes de rappel pour l'indexation des fichiers
@Client.on_callback_query(filters.regex(r'^index'))
async def index_files(bot, query):
    if query.data.startswith('index_cancel'):
        temp.CANCEL = True
        return await query.answer("Annulation de l'indexation")
    _, raju, chat, lst_msg_id, from_user = query.data.split("#")
    if raju == 'reject':
        await query.message.delete()
        await bot.send_message(int(from_user),
                               f'Votre soumission pour l\'indexation de {chat} a été rejetée par nos modérateurs.',
                               reply_to_message_id=int(lst_msg_id))
        return

    if lock.locked():
        return await query.answer('Veuillez attendre que le processus précédent soit terminé.', show_alert=True)
    msg = query.message

    await query.answer('Traitement en cours...⏳', show_alert=True)
    if int(from_user) not in ADMINS:
        await bot.send_message(int(from_user),
                               f'Votre soumission pour l\'indexation de {chat} a été acceptée par nos modérateurs et sera ajoutée bientôt.',
                               reply_to_message_id=int(lst_msg_id))
    await msg.edit(
        "Démarrage de l'indexation",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('Annuler', callback_data='index_cancel')]]
        )
    )
    try:
        chat = int(chat)
    except:
        chat = chat
    await index_files_to_db(int(lst_msg_id), chat, msg, bot)

# Fonction pour gérer l'envoi des fichiers pour indexation
@Client.on_message((filters.forwarded | (filters.regex("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")) & filters.text ) & filters.private & filters.incoming)
async def send_for_index(bot, message):
    if message.text:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(message.text)
        if not match:
            return await message.reply('Lien invalide')
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id  = int(("-100" + chat_id))
    elif message.forward_from_chat.type == enums.ChatType.CHANNEL:
        last_msg_id = message.forward_from_message_id
        chat_id = message.forward_from_chat.username or message.forward_from_chat.id
    else:
        return
    try:
        await bot.get_chat(chat_id)
    except ChannelInvalid:
        return await message.reply('Il se peut que ce soit un canal ou un groupe privé. Faites-moi administrateur pour indexer les fichiers.')
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('Lien invalide spécifié.')
    except Exception as e:
        logger.exception(e)
        return await message.reply(f'Erreurs - {e}')
    try:
        k = await bot.get_messages(chat_id, last_msg_id)
    except:
        return await message.reply('Assurez-vous que je suis administrateur dans le canal, si le canal est privé')
    if k.empty:
        return await message.reply('Il se peut que ce soit un groupe et je ne sois pas administrateur du groupe.')

    if message.from_user.id in ADMINS:
        buttons = [
            [
                InlineKeyboardButton('Oui',
                                     callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')
            ],
            [
                InlineKeyboardButton('Fermer', callback_data='close_data'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        return await message.reply(
            f"Voulez-vous indexer ce canal/groupe ?\n\nID/Username du chat : <code>{chat_id}</code>\nID du dernier message : <code>{last_msg_id}</code>",
            reply_markup=reply_markup)

    if type(chat_id) is int:
        try:
            link = (await bot.create_chat_invite_link(chat_id)).invite_link
        except ChatAdminRequired:
            return await message.reply('Assurez-vous que je suis administrateur dans le chat et que j\'ai la permission d\'inviter des utilisateurs.')
    else:
        link = f"@{message.forward_from_chat.username}"
    buttons = [
        [
            InlineKeyboardButton('Accepter l\'Indexation',
                                 callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')
        ],
        [
            InlineKeyboardButton('Rejeter l\'Indexation',
                                 callback_data=f'index#reject#{chat_id}#{message.id}#{message.from_user.id}'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await bot.send_message(LOG_CHANNEL,
                           f'#IndexRequest\n\nPar : {message.from_user.mention} (<code>{message.from_user.id}</code>)\nID/Username du chat - <code>{chat_id}</code>\nID du dernier message - <code>{last_msg_id}</code>\nInviteLink - {link}',
                           reply_markup=reply_markup)
    await message.reply('Merci pour votre contribution, attendez que mes modérateurs vérifient les fichiers.')

# Fonction de configuration du nombre de sauts de fichiers
@Client.on_message(filters.command('setskip') & filters.user(ADMINS))
async def set_skip_number(bot, message):
    if ' ' in message.text:
        _, skip = message.text.split(" ")
        try:
            skip = int(skip)
        except:
            return await message.reply("Le nombre de sauts doit être un entier.")
        await message.reply(f"Nombre de sauts défini avec succès à {skip}")
        temp.CURRENT = int(skip)
    else:
        await message.reply("Donnez-moi un nombre de sauts")

# Fonction pour indexer les fichiers dans la base de données
async def index_files_to_db(lst_msg_id, chat, msg, bot):
    total_files = 0
    duplicate = 0
    errors = 0
    deleted = 0
    no_media = 0
    unsupported = 0
    async with lock:
        try:
            current = temp.CURRENT
            temp.CANCEL = False
            async for message in bot.iter_messages(chat, lst_msg_id, temp.CURRENT):
                if temp.CANCEL:
                    await msg.edit(f"Indexation annulée avec succès !!\n\n<code>{total_files}</code> fichiers enregistrés dans la base de données !\nFichiers en double ignorés : <code>{duplicate}</code>\nMessages supprimés ignorés : <code>{deleted}</code>\nMessages non médiatiques ignorés : <code>{no_media + unsupported}</code>(Médias non pris en charge - `{unsupported}`)\nErreurs survenues : <code>{errors}</code>")
                    break
                current += 1
                if current % 20 == 0:
                    can = [[InlineKeyboardButton('Annuler', callback_data='index_cancel')]]
                    reply = InlineKeyboardMarkup(can)
                    await msg.edit_text(
                        text=f"Total des messages récupérés : <code>{current}</code>\nTotal des messages enregistrés : <code>{total_files}</code>\nFichiers en double ignorés : <code>{duplicate}</code>\nMessages supprimés ignorés : <code>{deleted}</code>\nMessages non médiatiques ignorés : <code>{no_media + unsupported}</code>(Médias non pris en charge - `{unsupported}`)\nErreurs survenues : <code>{errors}</code>",
                        reply_markup=reply)
                if message.empty:
                    deleted += 1
                    continue
                elif not message.media:
                    no_media += 1
                    continue
                elif message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT]:
                    unsupported += 1
                    continue
                media = getattr(message, message.media.value, None)
                if not media:
                    unsupported += 1
                    continue
                media.file_type = message.media.value
                media.caption = message.caption
                aynav, vnay = await save_file(media)
                if aynav:
                    total_files += 1
                elif vnay == 0:
                    duplicate += 1
                elif vnay == 2:
                    errors += 1
        except Exception as e:
            logger.exception(e)
            await msg.edit(f'Erreur : {e}')
        else:
            await msg.edit(f'Indexation réussie, <code>{total_files}</code> fichiers enregistrés dans la base de données !\nFichiers en double ignorés : <code>{duplicate}</code>\nMessages supprimés ignorés : <code>{deleted}</code>\nMessages non médiatiques ignorés : <code>{no_media + unsupported}</code>(Médias non pris en charge - `{unsupported}`)\nErreurs survenues : <code>{errors}</code>')
