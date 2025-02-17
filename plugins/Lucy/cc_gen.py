import asyncio
from pyrogram import Client, filters
import requests
from info import LOG_CHANNEL

@Client.on_message(filters.command("cc"))
async def google_text(client, message):
    try:
        user_query = message.text.split()[1:]
        if not user_query:
          await message.reply_text("Entrez quatre chiffres d'un bin pour créer la carte <code>/cc 1234</code>") 
          return
        response = requests.get(f"https://api.safone.dev/ccgen?bins={user_query}&limit=1")
        if response.status_code == 200:
            data = response.json()
            bin_data = data['results'][0]
            card = bin_data['cards']
            await client.send_message(message.chat.id, card)
            await client.send_message(LOG_CHANNEL, text=f"#ᴄᴄ_ɢᴇɴ\nHᴇʏ {message.from_user.mention}\nʟᴀ ᴅᴇᴍᴀɴᴅᴇ ᴇsᴛ {user_query}")

    except Exception as e:
       await message.reply_text(f"Une erreur s'est produite : {e}")