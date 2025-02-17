from info import ADMINS
from Script import Script
from time import time, sleep
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, UserAdminInvalid

@Client.on_message(filters.group & filters.command('inkick'))
async def inkick(client, message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        if len(message.command) > 1:
            input_str = message.command[1:]
            sent_message = await message.reply_text(Script.START_KICK)
            await sleep(20)
            await sent_message.delete()
            await message.delete()
            count = 0
            async for member in client.get_chat_members(message.chat.id):
                if member.user.status in input_str and not member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
                    try:
                        await client.ban_chat_member(message.chat.id, member.user.id, int(time() + 45))
                        count += 1
                        await sleep(1)
                    except (ChatAdminRequired, UserAdminInvalid):
                        await sent_message.edit(Script.ADMIN_REQUIRED)
                        await client.leave_chat(message.chat.id)
                        break
                    except FloodWait as e:
                        await sleep(e.x)
            try:
                await sent_message.edit(Script.KICKED.format(count))
            except ChatWriteForbidden:
                pass
        else:
            await message.reply_text(Script.INPUT_REQUIRED)
    else:
        sent_message = await message.reply_text(Script.CREATOR_REQUIRED)
        await sleep(5)
        await sent_message.delete()
        await message.delete()


@Client.on_message(filters.group & filters.command('dkick'))
async def dkick(client, message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        sent_message = await message.reply_text(Script.START_KICK)
        await sleep(20)
        await sent_message.delete()
        await message.delete()
        count = 0
        async for member in client.get_chat_members(message.chat.id):
            if member.user.is_deleted and not member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
                try:
                    await client.ban_chat_member(message.chat.id, member.user.id, int(time() + 45))
                    count += 1
                    await sleep(1)
                except (ChatAdminRequired, UserAdminInvalid):
                    await sent_message.edit(Script.ADMIN_REQUIRED)
                    await client.leave_chat(message.chat.id)
                    break
                except FloodWait as e:
                    await sleep(e.x)
        try:
            await sent_message.edit(Script.DKICK.format(count))
        except ChatWriteForbidden:
            pass
    else:
        sent_message = await message.reply_text(Script.CREATOR_REQUIRED)
        await sleep(5)
        await sent_message.delete()
        await message.delete()


@Client.on_message((filters.channel | filters.group) & filters.command('instatus'))
async def instatus(client, message):
    sent_message = await message.reply_text("🔁 Traitement en cours...")
    recently = 0
    within_week = 0
    within_month = 0
    long_time_ago = 0
    deleted_acc = 0
    uncached = 0
    bot = 0
    async for member in client.get_chat_members(message.chat.id, limit=int(10000)):
        user = member.user
        if user.is_deleted:
            deleted_acc += 1
        elif user.is_bot:
            bot += 1
        elif user.status == enums.UserStatus.RECENTLY:
            recently += 1
        elif user.status == enums.UserStatus.LAST_WEEK:
            within_week += 1
        elif user.status == enums.UserStatus.LAST_MONTH:
            within_month += 1
        elif user.status == enums.UserStatus.LONG_AGO:
            long_time_ago += 1
        else:
            uncached += 1

    chat_type = message.chat.type
    if chat_type == enums.ChatType.CHANNEL:
         await sent_message.edit(f"{message.chat.title}\nStatut des Membres du Chat\n\nRécemment - {recently}\nCette semaine - {within_week}\nCe mois-ci - {within_month}\nIl y a longtemps - {long_time_ago}\n\nCompte supprimé - {deleted_acc}\nBot - {bot}\nNon vérifié - {uncached}")            
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER, ADMINS):
            await sent_message.edit(f"{message.chat.title}\nStatut des Membres du Chat\n\nRécemment - {recently}\nCette semaine - {within_week}\nCe mois-ci - {within_month}\nIl y a longtemps - {long_time_ago}\n\nCompte supprimé - {deleted_acc}\nBot - {bot}\nNon vérifié - {uncached}")
        else:
            await sent_message.edit("Vous n'êtes pas administrateur dans ce chat")


class Script:
    # Messages pour le processus de kick
    START_KICK = "🔨 Démarrage du processus de kick..."
    INPUT_REQUIRED = "⚠️ Veuillez fournir un statut de membre à exclure (ex : 'recently', 'within_week', etc.)."
    ADMIN_REQUIRED = "⚠️ Vous devez être administrateur pour effectuer cette action."
    KICKED = "{} membres ont été exclus."
    CREATOR_REQUIRED = "⚠️ Seul le créateur du groupe peut utiliser cette commande."
    
    # Messages pour le processus de dkick (supprimer les membres supprimés)
    DKICK = "{} membres supprimés ont été exclus."
    
    # Messages pour le processus de status
    FETCHING_INFO = "🔄 Récupération des informations des membres en cours..."
    STATUS = """Statut du groupe {} :
    Membres récemment actifs : {}
    Membres actifs cette semaine : {}
    Membres actifs ce mois-ci : {}
    Membres inactifs depuis longtemps : {}
    Comptes supprimés : {}
    Bots : {}
    Membres non vérifiés : {}"""
