from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
import pytz
from info import ADMINS, LOG_CHANNEL, SUPPORT_CHAT, MELCOW_NEW_USERS, MELCOW_VID, CHNL_LNK, GRP_LNK
from database.users_chats_db import db
from database.ia_filterdb import Media
from utils import get_seconds, get_size, temp, get_settings
from Script import Script
from pyrogram.errors import ChatAdminRequired
import asyncio
import sys
from datetime import datetime, timedelta  # Importation correcte

sys.stdout.reconfigure(encoding='utf-8')

"""----------------------------------------- https://t.me/hyoshassistantbot --------------------------------------"""

@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    r_j_check = [u.id for u in message.new_chat_members]
    if temp.ME in r_j_check:
        if not await db.get_chat(message.chat.id):
            total=await bot.get_chat_members_count(message.chat.id)
            r_j = message.from_user.mention if message.from_user else "Anonymous" 
            await bot.send_message(LOG_CHANNEL, Script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, r_j))       
            await db.add_chat(message.chat.id, message.chat.title)
        if message.chat.id in temp.BANNED_CHATS:
            # Inspiré d'un bateau de bananier
            buttons = [[
                InlineKeyboardButton('Soutien', url='https://telegram.me/promo_premium_groupe')
            ]]
            reply_markup=InlineKeyboardMarkup(buttons)
            k = await message.reply(
                text='<b>Chat non autorisé 🐞\n\nMes administrateurs m\'ont restreint de travailler ici ! Si vous souhaitez en savoir plus, contactez le support.</b>',
                reply_markup=reply_markup,
            )

            try:
                await k.pin()
            except:
                pass
            await bot.leave_chat(message.chat.id)
            return
        buttons = [[
                    InlineKeyboardButton('Soutien', url='https://telegram.me/promo_premium_groupe'),
                    InlineKeyboardButton('Mises à jour', url='https://telegram.me/hyoshassistantbot')
                 ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=f"<b>›› Merci de m'avoir ajouté dans {message.chat.title} \n›› N'oubliez pas de me rendre administrateur.\n›› Si vous avez des doutes sur mon utilisation, cliquez sur le bouton ci-dessous</b>",
            reply_markup=reply_markup)
    else:
        settings = await get_settings(message.chat.id)
        if settings["welcome"]:
            for u in message.new_chat_members:
                if (temp.MELCOW).get('welcome') is not None:
                    try:
                        await (temp.MELCOW['welcome']).delete()
                    except:
                        pass
                temp.MELCOW['welcome'] = await message.reply_photo(
                                                 photo=(MELCOW_VID),
                                                 caption=(Script.MELCOW_ENG.format(u.mention, message.chat.title)),
                                                 reply_markup=InlineKeyboardMarkup(
                                                                         [[
                                                                           InlineKeyboardButton('• Rejoindre mes mises à jour •', url='https://t.me/hyoshassistantbot')
                                                                        ]]
                                                 ),
                                                 parse_mode=enums.ParseMode.HTML
                )
                
        if settings["auto_delete"]:
            await asyncio.sleep(600)
            await (temp.MELCOW['welcome']).delete()

@Client.on_message(filters.command('leave') & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Donne-moi un identifiant de chat')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        buttons = [[
            InlineKeyboardButton('Soutien', url='https://telegram.me/promo_premium_groupe')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat,
            text='<b>Bonjour amis, \nMon administrateur m\'a dit de quitter le groupe, donc je dois y aller !\nSi vous souhaitez m’ajouter à nouveau, contactez le support.</b>',
            reply_markup=reply_markup,
        )

        await bot.leave_chat(chat)
        await message.reply(f"J'ai quitté le chat `{chat}`")
    except Exception as e:
        await message.reply(f'Erreur - {e}')

@Client.on_message(filters.command('disable') & filters.user(ADMINS))
async def disable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Donne-moi un identifiant de chat')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "Aucune raison fournie"
    try:
        chat_ = int(chat)
    except:
        return await message.reply('Donne-moi un identifiant de chat valide')
    cha_t = await db.get_chat(int(chat_))
    if not cha_t:
        return await message.reply("Chat non trouvé dans la base de données")
    if cha_t['is_disabled']:
        return await message.reply(f"Ce chat est déjà désactivé :\nRaison-<code> {cha_t['reason']} </code>")
    await db.disable_chat(int(chat_), reason)
    temp.BANNED_CHATS.append(int(chat_))
    await message.reply('Chat désactivé avec succès')
    try:
        buttons = [[
            InlineKeyboardButton('Soutien', url='https://telegram.me/promo_premium_groupe')
        ]]

        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat_, 
            text=f'<b>Bonjour amis, \nMon administrateur m\'a dit de quitter le groupe, donc je dois y aller ! \nSi vous souhaitez m’ajouter à nouveau, contactez le support.</b> \nRaison : <code>{reason}</code>',
            reply_markup=reply_markup)
        await bot.leave_chat(chat_)
    except Exception as e:
        await message.reply(f"Erreur - {e}")

@Client.on_message(filters.command('enable') & filters.user(ADMINS))
async def re_enable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Donne-moi un identifiant de chat')
    chat = message.command[1]
    try:
        chat_ = int(chat)
    except:
        return await message.reply('Donne-moi un identifiant de chat valide')
    sts = await db.get_chat(int(chat))
    if not sts:
        return await message.reply("Chat non trouvé dans la base de données !")
    if not sts.get('is_disabled'):
        return await message.reply('Ce chat n\'est pas encore désactivé.')
    await db.re_enable_chat(int(chat_))
    temp.BANNED_CHATS.remove(int(chat_))
    await message.reply("Chat réactivé avec succès")

@Client.on_message(filters.command('stats') & filters.incoming)
async def get_ststs(bot, message):
    rju = await message.reply('Récupération des statistiques...')
    total_users = await db.total_users_count()
    totl_chats = await db.total_chat_count()
    files = await Media.count_documents()
    size = await db.get_db_size()
    free = 536870912 - size
    size = get_size(size)
    free = get_size(free)
    await rju.edit(Script.STATUS_TXT.format(files, total_users, totl_chats, size, free))

@Client.on_message(filters.command('invite') & filters.user(ADMINS))
async def gen_invite(bot, message):
    if len(message.command) == 1:
        return await message.reply('Donne-moi un identifiant de chat')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        return await message.reply('Donne-moi un identifiant de chat valide')
    try:
        link = await bot.create_chat_invite_link(chat)
    except ChatAdminRequired:
        return await message.reply("La génération du lien d'invitation a échoué, je n'ai pas les droits suffisants")
    except Exception as e:
        return await message.reply(f'Erreur {e}')
    await message.reply(f'Voici votre lien d\'invitation {link.invite_link}')

@Client.on_message(filters.command('ban') & filters.user(ADMINS))
async def ban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('Donne-moi un ID d\'utilisateur / nom d\'utilisateur')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "Aucune raison fournie"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("C'est un utilisateur invalide, assure-toi de l'avoir déjà rencontré.")
    except IndexError:
        return await message.reply("Cela pourrait être un canal, assure-toi que c'est un utilisateur.")
    except Exception as e:
        return await message.reply(f'Erreur - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if jar['is_banned']:
            return await message.reply(f"{k.mention} est déjà banni\nRaison: {jar['ban_reason']}")
        await db.ban_user(k.id, reason)
        temp.BANNED_USERS.append(k.id)
        await message.reply(f"{k.mention} a été banni avec succès")

@Client.on_message(filters.command('unban') & filters.user(ADMINS))
async def unban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('Donne-moi un ID d\'utilisateur / nom d\'utilisateur')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "Aucune raison fournie"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("C'est un utilisateur invalide, assure-toi de l'avoir déjà rencontré.")
    except IndexError:
        return await message.reply("Cela pourrait être un canal, assure-toi que c'est un utilisateur.")
    except Exception as e:
        return await message.reply(f'Erreur - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if not jar['is_banned']:
            return await message.reply(f"{k.mention} n'est pas encore banni.")
        await db.remove_ban(k.id)
        temp.BANNED_USERS.remove(k.id)
        await message.reply(f"{k.mention} a été débanni avec succès")

@Client.on_message(filters.command('users') & filters.user(ADMINS))
async def list_users(bot, message):
    raju = await message.reply('Obtention de la liste des utilisateurs')
    users = await db.get_all_users()
    out = "Les utilisateurs enregistrés dans la base de données sont :\n\n"
    async for user in users:
        out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>"
        if user['ban_status']['is_banned']:
            out += '( Utilisateur banni )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('users.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt', caption="Liste des utilisateurs")

@Client.on_message(filters.command('chats') & filters.user(ADMINS))
async def list_chats(bot, message):
    raju = await message.reply('Obtention de la liste des chats')
    chats = await db.get_all_chats()
    out = "Les chats enregistrés dans la base de données sont :\n\n"
    async for chat in chats:
        out += f"**Titre :** `{chat['title']}`\n**- ID :** `{chat['id']}`"
        if chat['chat_status']['is_disabled']:
            out += '( Chat désactivé )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('chats.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('chats.txt', caption="Liste des chats")
        
@Client.on_message(filters.command("remove_premium") & filters.user(ADMINS))
async def remove_premium(client, message):
    if len(message.command) == 2:
        try:
            user_id = int(message.command[1])  # Convertir l'ID utilisateur en entier
            user = await client.get_users(user_id)
            if await db.remove_premium_access(user_id):
                await message.reply_text("L'accès premium de l'utilisateur a été supprimé avec succès !")
                await client.send_message(
                    chat_id=user_id,
                    text=f"<b>Hé {user.mention},\n\nTon accès premium a été supprimé.\nMerci d'avoir utilisé notre service 😊\nClique sur /plan pour voir d'autres plans.</b>"
                )
            else:
                await message.reply_text("Impossible de supprimer cet utilisateur !\nEs-tu sûr qu'il s'agissait d'un utilisateur premium ?")
        except Exception as e:
            await message.reply_text(f"Erreur : {e}")
    else:
        await message.reply_text("UTILISATION : /remove_premium user_id")
        

@Client.on_message(filters.command("myplan"))
async def myplan(client, message):
    user = message.from_user.mention
    print(user)
    user_id = message.from_user.id
    print(user_id)
    data = await db.get_user(user_id)
    if data and data.get("expiry_time"):
        expiry = data.get("expiry_time")
        expiry_ist = expiry.astimezone(pytz.timezone("UTC"))
        expiry_str_in_ist = expiry_ist.strftime("%d-%m-%Y\n Heure d'expiration : %I:%M:%S %p")
        
        current_time = datetime.now(pytz.timezone("UTC"))
        time_left = expiry_ist - current_time

        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        time_left_str = f"{days} jours, {hours} heures, {minutes} minutes"
        await message.reply_text(f"⚜️ Données utilisateur premium :\n\n👤 Utilisateur : {user}\n⚡ ID utilisateur : <code>{user_id}</code>\n⏰ Temps restant : {time_left_str}\n⌛️ Date d'expiration : {expiry_str_in_ist}")
    else:
        await message.reply_text(f"Hé {user},\n\nTu n'as pas de plan premium actif. Si tu veux obtenir un plan premium, clique sur le bouton ci-dessous 👇", 
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💸 Voir les plans premium 💸", callback_data='seeplans')]]))
        
@Client.on_message(filters.command("get_premium") & filters.user(ADMINS))
async def get_premium(client, message):
    if len(message.command) == 2:
        try:
            user_id = int(message.command[1])
            user = await client.get_users(user_id)
            data = await db.get_user(user_id)
            if data and data.get("expiry_time"):
                expiry = data.get("expiry_time")
                expiry_ist = expiry.astimezone(pytz.timezone("UTC"))
                expiry_str_in_ist = expiry_ist.strftime("%d-%m-%Y\n Heure d'expiration : %I:%M:%S %p")

                current_time = datetime.now(pytz.timezone("UTC"))
                time_left = expiry_ist - current_time

                days = time_left.days
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                time_left_str = f"{days} jours, {hours} heures, {minutes} minutes"
                await message.reply_text(f"⚜️ Données utilisateur premium :\n\n👤 Utilisateur : {user.mention}\n⚡ ID utilisateur : <code>{user_id}</code>\n⏰ Temps restant : {time_left_str}\n⌛️ Date d'expiration : {expiry_str_in_ist}")
            else:
                await message.reply_text("Aucune donnée premium trouvée dans la base de données !")
        except Exception as e:
            await message.reply_text(f"Erreur : {e}")
    else:
        await message.reply_text("UTILISATION : /get_premium user_id")

@Client.on_message(filters.command("add_premium") & filters.user(ADMINS))
async def give_premium_cmd_handler(client, message):
    if len(message.command) == 4:
        try:
            time_zone = datetime.now(pytz.timezone("UTC"))
            current_time = time_zone.strftime("%d-%m-%Y\n Heure d'entrée : %I:%M:%S %p")
            user_id = int(message.command[1])  # Convertir l'ID utilisateur en entier
            user = await client.get_users(user_id)
            time = message.command[2] + " " + message.command[3]
            seconds = await get_seconds(time)
            if seconds > 0:
                expiry_time = datetime.now() + timedelta(seconds=seconds)  # Utilisation correcte de timedelta
                user_data = {"id": user_id, "expiry_time": expiry_time}  
                await db.update_user(user_data)  # Mettre à jour ou insérer les données utilisateur
                data = await db.get_user(user_id)
                expiry = data.get("expiry_time")   
                expiry_str_in_ist = expiry.astimezone(pytz.timezone("UTC")).strftime("%d-%m-%Y\n Heure d'expiration : %I:%M:%S %p")
                await message.reply_text(f"Premium ajouté avec succès ✅\n\n👤 Utilisateur : {user.mention}\n⚡ ID utilisateur : <code>{user_id}</code>\n⏰ Accès premium : <code>{time}</code>\n\n⏳ Heure d'entrée : {current_time}\n\n⌛️ Date d'expiration : {expiry_str_in_ist}", disable_web_page_preview=True)
                await client.send_message(
                    chat_id=user_id,
                    text=f"👋 Hé {user.mention},\nMerci d'avoir acheté premium.\nTon accès premium a été activé et expire le {expiry_str_in_ist}."
                )
            else:
                await message.reply_text("Le temps fourni est invalide !")
        except Exception as e:
            await message.reply_text(f"Erreur : {e}")
    else:
        await message.reply_text("UTILISATION : /add_premium user_id temps (ex: 1 day)")
        