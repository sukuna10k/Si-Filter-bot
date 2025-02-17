import os
import time
from asyncio import sleep
from pyrogram import Client, filters
from pyrogram import enums, filters

@Client.on_message(~filters.private & filters.command(["groupdata"]), group=2)
async def instatus(Client, message):
    start_time = time.perf_counter()
    user = await Client.get_chat_member(message.chat.id, message.from_user.id)
    count = await Client.get_chat_members_count(message.chat.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        sent_message = await message.reply_text("Récupération des informations...")
        deleted_acc = 0
        premium_acc = 0
        banned = 0
        bot = 0
        uncached = 0
        async for ban in Client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BANNED):
            banned += 1
        async for member in Client.get_chat_members(message.chat.id):
            user = member.user
            if user.is_deleted:
                deleted_acc += 1
            elif user.is_bot:
                bot += 1
            elif user.is_premium:
                premium_acc += 1
            else:
                uncached += 1
        end_time = time.perf_counter()
        timelog = "{:.2f}".format(end_time - start_time)
        await sent_message.edit(f"""
**➖➖➖➖➖➖➖
➲ Nom : {message.chat.title} ✅
➲ Membres : [ {count} ]🫂
➖➖➖➖➖➖➖
➲ Bots : {bot}💡
➲ Comptes supprimés : {deleted_acc}🧟
➲ Bannies : {banned}🚫
➲ Utilisateurs premium : {premium_acc}🎁
➖➖➖➖➖➖➖
Temps de traitement : {timelog} S**""")
    else:
        sent_message = await message.reply_text("SEULS LES ADMINS PEUVENT UTILISER CETTE COMMANDE !")
        await sleep(5)
        await sent_message.delete()
