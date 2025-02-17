from openai import OpenAI
from pyrogram import Client, filters
from pyrogram.types import Message

MODEL_INFO = {
    "nom": "DeepSeek R1",
    "créateur": "@hyoshcoder",
    "version": "1.0",
    "description": "Un modèle IA avancé basé sur DeepSeek R1 pour répondre à vos questions.",
}

DEEPSEEK_API_KEY = "sk-badafa01878c4e59bb6f2341f7c319fe"

deepseek_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

@Client.on_message(filters.command("deepseek"))
async def ask(client: Client, message: Message):
    """Répond aux questions des utilisateurs via l'API DeepSeek R1."""
    
    if len(message.command) < 2:
        return await message.reply_text("❌ **Erreur :** Veuillez fournir une requête après la commande `/ask`.")

    query = " ".join(message.command[1:])
    thinking_message = await message.reply_text("⏳ **Veuillez patienter...**")

    keywords = ["nom", "créateur", "version", "description", "info", "informations"]
    if any(mot in query.lower() for mot in keywords):
        response = (
            f"ℹ️ **Informations sur le modèle :**\n\n"
            f"📌 **Nom :** {MODEL_INFO['nom']}\n"
            f"👨‍💻 **Créateur :** {MODEL_INFO['créateur']}\n"
            f"📅 **Version :** {MODEL_INFO['version']}\n"
            f"📝 **Description :** {MODEL_INFO['description']}\n"
        )
        return await thinking_message.edit(response)

    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Vous êtes un assistant IA avancé."},
                {"role": "user", "content": query},
            ],
            stream=False
        )

        result = response.choices[0].message.content
        final_response = (
            f"👤 **Utilisateur :** {message.from_user.mention}\n"
            f"💬 **Requête :** `{query}`\n"
            f"──────────────\n"
            f"🤖 **Réponse :**\n{result}"
        )

        await thinking_message.edit(final_response)

    except Exception as e:
        error_message = f"❌ **Une erreur est survenue :**\n`{str(e)[:100]}...`\n\n🚀 *Essayez plus tard ou contactez @hyoshcoder*."
        await thinking_message.edit(error_message)
