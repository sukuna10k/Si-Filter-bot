from info import ADMINS
from Script import Script
from time import time, sleep
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, UserAdminInvalid

async def handle_kick(client, message, kick_condition, kick_message, kick_format):
    """Fonction pour gérer le kick des membres selon un critère spécifique."""
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status != "creator":
        sent_message = await message.reply_text(Script.CREATOR_REQUIRED)
        sleep(5)
        await sent_message.delete()
        return await message.delete()

    if len(message.command) <= 1:
        return await message.reply_text(kick_message)

    input_str = message.command[1:]
    sent_message = await message.reply_text(Script.START_KICK)
    sleep(2)  # Réduction de l'attente pour éviter trop de latence
    await sent_message.delete()
    await message.delete()

    count = 0
    for member in client.iter_chat_members(message.chat.id):
        if kick_condition(member, input_str):
            try:
                await client.kick_chat_member(message.chat.id, member.user.id, int(time() + 45))
                count += 1
                sleep(1)  # Contrôler les appels pour éviter d'être bloqué par l'API
            except (ChatAdminRequired, UserAdminInvalid):
                await sent_message.edit(Script.ADMIN_REQUIRED)
                await client.leave_chat(message.chat.id)
                break
            except FloodWait as e:
                sleep(e.x)

    try:
        await sent_message.edit(kick_format.format(count))
    except ChatWriteForbidden:
        pass

@Client.on_message(filters.incoming & ~filters.private & filters.command('inkick'))
async def inkick(client, message):
    """Kick des membres selon leur statut."""
    await handle_kick(client, message, 
                      lambda member, input_str: member.user.status in input_str and member.status not in ('administrator', 'creator'),
                      Script.INPUT_REQUIRED,
                      Script.KICKED)

@Client.on_message(filters.incoming & ~filters.private & filters.command('dkick'))
async def dkick(client, message):
    """Kick des membres supprimés."""
    await handle_kick(client, message, 
                      lambda member, input_str: member.user.is_deleted and member.status not in ('administrator', 'creator'),
                      Script.INPUT_REQUIRED,
                      Script.DKICK)

@Client.on_message(filters.incoming & ~filters.private & filters.command('instatus'))
async def instatus(client, message):
    """Récupère et affiche le statut des membres du groupe."""
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in ('administrator', 'creator') and message.from_user.id not in ADMINS:
        return await message.reply_text(Script.ADMIN_REQUIRED)

    sent_message = await message.reply_text(Script.FETCHING_INFO)
    status_counts = {"recently": 0, "within_week": 0, "within_month": 0, "long_time_ago": 0, "deleted_acc": 0, "uncached": 0, "bot": 0}

    for member in client.iter_chat_members(message.chat.id):
        user = member.user
        if user.is_deleted:
            status_counts["deleted_acc"] += 1
        elif user.is_bot:
            status_counts["bot"] += 1
        elif user.status in status_counts:
            status_counts[user.status] += 1
        else:
            status_counts["uncached"] += 1

    await sent_message.edit(Script.STATUS.format(message.chat.title,
                                                 status_counts["recently"], 
                                                 status_counts["within_week"], 
                                                 status_counts["within_month"], 
                                                 status_counts["long_time_ago"],
                                                 status_counts["deleted_acc"], 
                                                 status_counts["bot"],
                                                 status_counts["uncached"]))

class Script:
    # Messages pour le processus de kick
    START_KICK = "Démarrage du processus de kick..."
    INPUT_REQUIRED = "Veuillez fournir un statut de membre à exclure (ex : 'recently', 'within_week', etc.)."
    ADMIN_REQUIRED = "Vous devez être un administrateur pour effectuer cette action."
    KICKED = "{} membres ont été exclus."
    CREATOR_REQUIRED = "Seul le créateur du groupe peut utiliser cette commande."
    
    # Messages pour le processus de dkick (supprimer les membres supprimés)
    DKICK = "{} membres supprimés ont été exclus."
    
    # Messages pour le processus de status
    FETCHING_INFO = "Récupération des informations des membres en cours..."
    STATUS = """Statut du groupe {} :
    Membres récemment actifs : {}
    Membres actifs cette semaine : {}
    Membres actifs ce mois-ci : {}
    Membres inactifs depuis longtemps : {}
    Comptes supprimés : {}
    Bots : {}
    Membres non vérifiés : {}"""
