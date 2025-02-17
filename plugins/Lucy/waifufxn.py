from pyrogram import Client, filters
import requests


# Fonction pour récupérer l'URL de l'animation depuis l'API
def get_animation(api_token, animation_type):
    url = f"https://waifu.it/api/v4/{animation_type}"
    headers = {"Authorization": api_token}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("url")
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite lors de la requête : {e}")
        return None
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {str(e)}")
        return None

# Gestionnaires de commandes pour diverses animations
@Client.on_message(filters.command(["punch", "slap", "lick", "kill", "kick", "hug", "bite", "kiss", "highfive"]) & ~filters.forwarded & ~filters.via_bot)
def animation_command(client, message):
    try:
        sender = message.from_user.mention(style='markdown')
        target = sender if not message.reply_to_message else message.reply_to_message.from_user.mention(style='markdown')
        
        commands = {
            "punch": {"emoji": "💥", "text": "a frappé"},
            "slap": {"emoji": "😒", "text": "a giflé"},
            "lick": {"emoji": "😛", "text": "a léché"},
            "kill": {"emoji": "😵", "text": "a tué"},
            "kick": {"emoji": "😠", "text": "a donné un coup de pied à"},
            "hug": {"emoji": "🤗", "text": "a enlacé"},
            "bite": {"emoji": "😈", "text": "a mordu"},
            "kiss": {"emoji": "😘", "text": "a embrassé"},
            "highfive": {"emoji": "🙌", "text": "a tapé dans la main de"}
        }

        command = message.command[0].lower()
        api_token = "MTIyMDIyOTIxNjQ4Mjg4OTc0OA--.MTcxMDk5NTgxMA--.fb82de684cd7"
        gif_url = get_animation(api_token, command)

        if gif_url:
            msg = f"{sender} {commands[command]['text']} {target}! {commands[command]['emoji']}"
            message.reply_animation(animation=gif_url, caption=msg)
        else:
            message.reply_text("Impossible de récupérer l'animation. Veuillez réessayer.")
        
    except Exception as e:
        message.reply_text(f"Une erreur inattendue s'est produite : {str(e)}")
