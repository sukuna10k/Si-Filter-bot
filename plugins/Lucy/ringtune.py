import os
import logging
from pyrogram import Client, filters, enums
import requests
import json
from info import LOG_CHANNEL


@Client.on_message(filters.command("ringtune"))
async def music(client, message):

    query = " ".join(message.command[1:])


    if not query:
        await client.send_message(message.chat.id, "Veuillez fournir un nom de chanson à rechercher. Utilisation : /ringtune (nom_de_chanson) ou (nom_de_chanson + nom_de_l'artiste)")
        return

    try:
  
        response = requests.get(f"https://api.deezer.com/search?q={query}")


        response.raise_for_status()


        result = response.json()


        if "data" not in result or not result["data"]:
            await client.send_message(message.chat.id, f"Aucun résultat trouvé pour {query}.")
            return

        song = result["data"][0]

 
        song_info = {
            "artist": song["artist"]["name"],
            "title": song["title"],
            "duration": song["duration"],
            "preview_url": song["preview"],
        }


        await client.send_message(message.chat.id, f"Salut {message.from_user.mention},\n\nVotre demande {query}\n\n🎤 Artiste : {song_info['artist']}\n🎧 Titre : {song_info['title']}\n⌛ Durée : {song_info['duration']} secondes\n\nVous pouvez télécharger cette chanson depuis Chrome : {song_info['preview_url']}")


        await client.send_chat_action(message.chat.id, "upload_audio")

  
        if message.reply_to_message and message.reply_to_message.media:

            await client.send_audio(message.chat.id, song_info['preview_url'], title=song_info['title'], performer=song_info['artist'], reply_to_message_id=message.reply_to_message.id)
        else:

            await client.send_audio(message.chat.id, song_info['preview_url'], title=song_info['title'], performer=song_info['artist'], reply_to_message_id=message.id)
    except requests.RequestException as e:

        logging.error(f"Erreur lors de la récupération des informations de la chanson : {e}")
        await client.send_message(message.chat.id, "Une erreur s'est produite lors de la récupération des informations de la chanson. Veuillez réessayer plus tard.")
        await client.send_message(LOG_CHANNEL, text=f"#ringtune\nDemandé par {message.from_user.mention}\nLa demande est {query}")
