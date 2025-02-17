from pyrogram import Client, filters
from pyrogram.types import Message
from info import ADMINS, LOG_CHANNEL, SUPPORT_CHAT_ID
import asyncio

@Client.on_message(filters.private & filters.command("admin"))
async def forward_message_to_group(client, message):
 try:
    text = message.text.split(" ", 1)[1] 
    user_id = message.from_user.id
    name = message.from_user.mention
    await message.forward(LOG_CHANNEL)
    await client.send_message(LOG_CHANNEL, text=f"Un nouveau message de {name}\n\nID Utilisateur= <code>{user_id}</code>")
    await client.send_message(LOG_CHANNEL, text=f"Si vous voulez répondre, utilisez cette commande\n\n<code>!ans {user_id} votre_message</code>")
    success_message = await message.reply_text("Message transféré aux administrateurs. Attendez la réponse.")

 except Exception as e:
    await message.reply_text(f"Erreur {e}")

@Client.on_message(filters.command("ans", "!") & filters.user(ADMINS) & filters.chat(int(SUPPORT_CHAT_ID)))
async def reply_to_forwarded_message(client, message:Message):
 try: 
    mrtg = message.text.split(" ", 2)
    user_id = int(mrtg[1])
    reply_text = mrtg[2]
    await client.send_message(user_id, text=f"Réponse de mon administrateur")
    await client.send_message(user_id, text=f"<code>{reply_text}</code>")
    await message.reply_text(f"Message envoyé avec succès à <a href='tg://user?id={user_id}'><b>Utilisateur</b></a>")
 except Exception as e:
    await message.reply_text(f"Erreur {e}")
