import asyncio
from pyrogram import Client, filters
import requests
from info import LOG_CHANNEL

@Client.on_message(filters.command("torrent"))
async def google_text(client, message):
    try:
        user_query = message.text.split()[1:]
        if not user_query:
            await message.reply_text("Veuillez fournir un nom de film, <code>/torrent votre nom</code>")
            return 
        encoded_query = " ".join(user_query).replace(" ", "")

        response = requests.get(f"https://api.safone.dev/torrent?query={encoded_query}&limit=1")
        if response.status_code == 200:
            data = response.json()
            torrent_r = data['results'][0]
          
            tor = f"**Nom du fichier :**<code>{torrent_r['name']}</code>\n\n"\
                  f"**🔖 Taille :** <code>{torrent_r['size']}</code>\n" \
                  f"**🔗 Type :** {torrent_r['type']}\n" \
                  f"**✨ Langue :** <code>{torrent_r['language']}</code>\n" \
                  f"**📡 Lien Magnet :** <code>{torrent_r['magnetLink']}</code>"
    
            await client.send_message(message.chat.id, tor)
            await client.send_message(LOG_CHANNEL, text=f"#ᴛᴏʀʀᴇɴᴛ\nSalut {message.from_user.mention}\nLa requête est {user_query}")
    except Exception as e:
       await message.reply_text(f"Une erreur s'est produite : {e}")
