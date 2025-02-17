import re
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from info import OWNER_ID


@Client.on_message(filters.video_chat_started)
async def video_chat_started_handler(_: Client, msg: Message):
    await msg.reply("📹 La discussion vidéo a commencé.")

@Client.on_message(filters.video_chat_ended)
async def video_chat_ended_handler(_: Client, msg: Message):
    await msg.reply("❌ **La discussion vidéo est terminée.**")

@Client.on_message(filters.video_chat_members_invited)
async def video_chat_members_invited_handler(_: Client, message: Message):
    invited_users = message.video_chat_members_invited.users
    if invited_users:
        text = f"{message.from_user.mention} a invité :\n"
        text += "\n".join([f"[{user.first_name}](tg://user?id={user.id})" for user in invited_users])
        await message.reply(f"{text} 😉")

@Client.on_message(filters.command("math", prefixes="/"))
async def calculate_math(client: Client, message: Message):
    try:
        expression = message.text.split(maxsplit=1)[1]
        result = eval(expression, {"__builtins__": None}, {})
        await message.reply(f"📊 Le résultat est : <code>{result}</code>")
    except (IndexError, SyntaxError, NameError):
        await message.reply("❌ Expression invalide. Utilisation : `/math 2+2`")
    except Exception as e:
        await message.reply(f"❌ Une erreur est survenue : {str(e)}")

@Client.on_message(filters.command("leavegrp") & filters.user(OWNER_ID))
async def bot_leave(client: Client, message: Message):
    chat_id = message.chat.id
    await message.reply_text("👋 Le bot a quitté le groupe avec succès.")
    await client.leave_chat(chat_id, delete=True)

@Client.on_message(filters.command(["spg"], prefixes=["/", "!", "."]))
async def google_search(client: Client, message: Message):
    query = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None

    if not query:
        await message.reply("❌ Veuillez fournir un terme de recherche.")
        return

    msg = await message.reply("🔍 Recherche en cours...")
    search_url = "https://content-customsearch.googleapis.com/customsearch/v1"
    params = {
        "cx": "ec8db9e1f9e41e65e",
        "q": query,
        "key": "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM",
        "start": 1
    }
    headers = {"x-referer": "https://explorer.apis.google.com"}

    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, params=params, headers=headers) as response:
            if response.status != 200:
                await msg.edit("❌ Erreur lors de la récupération des résultats.")
                return

            data = await response.json()
            results = data.get("items", [])
            
            if not results:
                await msg.edit("Aucun résultat trouvé !")
                return
            
            result_text = ""
            seen_links = set()
            for item in results:
                title = item.get("title")
                link = item.get("link")
                link = re.sub(r'\/\d', "", link.split("?")[0])  

                if link in seen_links:
                    continue  
                seen_links.add(link)
                
                result_text += f"🔗 <b>{title}</b>\n{link}\n\n"

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("▶️ Suivant", callback_data=f"next 11 {query}")]
            ])
            await msg.edit(result_text, link_preview=False, reply_markup=keyboard)
