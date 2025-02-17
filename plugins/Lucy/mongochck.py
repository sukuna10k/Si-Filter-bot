from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
import re


mongo_url_pattern = re.compile(r'mongodb(?:\+srv)?:\/\/[^\s]+')


@Client.on_message(filters.command("mongo"))
async def mongo_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply("Veuillez entrer votre URL MongoDB après la commande. Exemple : /mongo votre_url_mongodb")
        return

    mongo_url = message.command[1]
    if re.match(mongo_url_pattern, mongo_url):
        try:
            # Attempt to connect to the MongoDB instance
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            client.server_info()  # Will cause an exception if connection fails
            await message.reply("L'URL MongoDB est valide et la connexion est réussie ✅")
        except Exception as e:
            await message.reply(f"Échec de la connexion à MongoDB : {e}")
    else:
        await message.reply("Format d'URL MongoDB invalide 💔")
