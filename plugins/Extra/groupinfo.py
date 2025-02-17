from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("groupinfo", prefixes="/"))
async def get_group_status(client: Client, message: Message):
    if len(message.command) != 2:
        await message.reply("Veuillez fournir un nom d'utilisateur de groupe. Exemple : `/groupinfo VotreNomDeGroupe`")
        return
    
    group_username = message.command[1]
    
    try:
        group = await client.get_chat(group_username)
        total_members = await client.get_chat_members_count(group.id)
    except Exception as e:
        await message.reply(f"Erreur : {e}")
        return

    group_description = group.description or "Aucune description disponible"
    
    response_text = (
        f"➖➖➖➖➖➖➖\n"
        f"➲ NOM DU GROUPE : {group.title} ✅\n"
        f"➲ ID DU GROUPE : {group.id}\n"
        f"➲ MEMBRES AU TOTAL : {total_members}\n"
        f"➲ DESCRIPTION : {group_description}\n"
        f"➲ NOM D'UTILISATEUR : @{group_username}\n"
        f"➖➖➖➖➖➖➖"
    )
    
    await message.reply(response_text)

@Client.on_message(filters.command("status") & filters.group)
async def group_status(client: Client, message: Message):
    chat = message.chat  
    status_text = (
        f"ID du groupe : {chat.id}\n"
        f"Titre : {chat.title}\n"
        f"Type : {chat.type}\n"
    )

    if chat.username:
        status_text += f"Nom d'utilisateur : @{chat.username}"
    else:
        status_text += "Nom d'utilisateur : Aucun"

    await message.reply_text(status_text)

