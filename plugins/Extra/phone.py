from pyrogram import Client, filters
import aiohttp
import json

API_KEY = "f66950368a61ebad3cba9b5924b4532d"
API_URL = "http://apilayer.net/api/validate"

def send_message(message, text):
    """Envoie un message en réponse."""
    message.reply_text(text)

@Client.on_message(filters.command("phone"))
async def check_phone(client, message):
    try:
        args = message.text.split(None, 1)
        if len(args) < 2:
            return await message.reply_text("❌ Veuillez fournir un numéro de téléphone.\nExemple : `/phone +33123456789`")

        number = args[1].strip()
        
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, params={
                "access_key": API_KEY,
                "number": number,
                "country_code": "",
                "format": "1"
            }) as response:
                if response.status != 200:
                    return await message.reply_text("❌ Erreur lors de la vérification du numéro.")

                data = await response.json()

                if not data.get("valid"):
                    return await message.reply_text("❌ Le numéro fourni est invalide.")

                country_code = data.get("country_code", "N/A")
                country_name = data.get("country_name", "N/A")
                location = data.get("location", "N/A")
                carrier = data.get("carrier", "N/A")
                line_type = data.get("line_type", "N/A")

                response_text = (
                    f"✅ **Informations sur le numéro**\n"
                    f"📞 **Numéro :** `{number}`\n"
                    f"🏳️ **Code pays :** `{country_code}`\n"
                    f"🌍 **Pays :** `{country_name}`\n"
                    f"📍 **Emplacement :** `{location}`\n"
                    f"📡 **Opérateur :** `{carrier}`\n"
                    f"☎️ **Type de ligne :** `{line_type}`\n"
                )
                await message.reply_text(response_text, parse_mode="markdown")

    except Exception as e:
        await message.reply_text(f"❌ Une erreur s'est produite : {e}")
