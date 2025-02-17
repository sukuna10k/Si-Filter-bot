from pyrogram import Client, filters,enums
import aiohttp

@Client.on_message(filters.command("meme"))
async def meme_command(client: Client, message):
    api_url = "https://meme-api.com/gimme"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    await message.reply_text("❌ Impossible de récupérer un meme pour le moment.")
                    return

                data = await response.json()
                meme_url = data.get("url")
                title = data.get("title", "Mème sans titre")

                if not meme_url:
                    await message.reply_text("❌ Aucun mème trouvé. Réessayez plus tard.")
                    return

                caption = (
                    f"<b>{title}</b>\n\n"
                    f"📤 Demandé par {message.from_user.mention}\n"
                    f"🔔 Mises à jour : @hyoshassistantbot"
                )

                await message.reply_photo(photo=meme_url, caption=caption, parse_mode=enums.ParseMode.HTML)

    except Exception as e:
        print(f"Erreur lors de la récupération du meme : {e}")
        await message.reply_text("❌ Une erreur s'est produite lors de la récupération du mème.")
