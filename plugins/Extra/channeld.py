from pyrogram import Client, filters, enums
from pyrogram.types import Message

@Client.on_message(filters.private & filters.forwarded)
async def info(client: Client, msg: Message):
    if msg.forward_from:
        user = msg.forward_from
        text = "<u>Informations de transfert 👀</u>\n\n"
        text += "<u>🤖 Informations du bot</u>" if user.is_bot else "<u>👤 Informations de l'utilisateur</u>"

        text += f"\n\n👨‍💼 Nom : {user.first_name}"
        text += f"\n\n🔗 Nom d'utilisateur : @{user.username}" if user.username else ""
        text += f"\n\n🆔 ID : <code>{user.id}</code>"
        text += f"\n\n💫 DC : {user.dc_id}"

        await msg.reply(text, quote=True)

    elif msg.forward_sender_name:
        # Gestion des messages transférés depuis des comptes anonymes
        await msg.reply(f"❌️Erreur : <b><i>{msg.forward_sender_name}</i></b> ❌️", quote=True)

    elif msg.forward_from_chat:
        chat = msg.forward_from_chat
        chat_type = chat.type
        text = "<u>Informations de transfert 👀</u>\n\n"

        if chat_type == enums.ChatType.CHANNEL:
            text += "<u>📢 Canal</u>"
        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            text += "<u>🗣️ Groupe</u>"

        text += f"\n\n📃 Nom : {chat.title}"
        text += f"\n\n➡️ De : @{chat.username}" if chat.username else ""
        text += f"\n\n🆔 ID : <code>{chat.id}</code>"
        text += f"\n\n💫 DC : {chat.dc_id}"

        await msg.reply(text, quote=True)

    else:
        await msg.reply("❌ Aucune information disponible sur le message transféré.", quote=True)
