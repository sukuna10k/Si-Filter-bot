import secureme
from pyrogram import Client, filters


@Client.on_message(filters.command("encrypt"))
async def encyrpt(bot, message):
    if len(message.command) < 2:
        return await message.reply_text("**Exemple:**\n\n`/encyrpt India`")
    m = message.text.split(' ',1)[1]
    try:
        Secure = secureme.encrypt(m)
        
        await message.reply_text(f"`{Secure}`")
        

    except Exception as e:
        await message.reply_text(f"Erreur {e}")

@Client.on_message(filters.command("decrypt"))
async def decrypt(bot, message):
    if len(message.command) < 2:
        return await message.reply_text("**Exemple:**\n\n`/decrypt Nsinf`")
    m = message.text.split(' ',1)[1]
    try:
        Decrypt = secureme.decrypt(m)
        
        await message.reply_text(f"`{Decrypt}`")
        

    except Exception as e:
        await message.reply_text(f"Erreur {e}")


__mod_name__ = "ᴍᴏᴛ ᴅᴇ ᴘᴀssᴇ"

__help__ = """
*ᴄᴏɴᴠᴇʀᴛɪᴛ*
 ❍ /encrypt*:* ᴄʀʏᴘᴛᴇ ʟᴇ ᴛᴇxᴛᴇ ᴅᴏɴɴé
 ❍ /decrypt*:* ᴅéᴄʀʏᴘᴛᴇ ʟᴇ ᴛᴇxᴛᴇ ᴘʀéᴄéᴅᴇᴍᴍᴇɴᴛ ᴄʀʏᴘᴛé
 ❍ /encode*:* ᴄᴏᴅᴇ ʟᴇ ᴛᴇxᴛᴇ ᴅᴏɴɴé
 ❍ /decode*:* ᴅéᴄᴏᴅᴇ ʟᴇ ᴛᴇxᴛᴇ ᴘʀéᴄéᴅᴇᴍᴍᴇɴᴛ ᴄʀʏᴘᴛé
 ❍ /morseencode*:* ᴄᴏᴅᴇ ᴍᴏʀsᴇ ʟᴇ ᴛᴇxᴛᴇ ᴅᴏɴɴé
 ❍ /morsedecode*:* ᴅéᴄʀʏᴘᴛᴇ ʟᴇ ᴛᴇxᴛᴇ ᴘʀéᴄéᴅᴇᴍᴍᴇɴᴛ ᴄʀʏᴘᴛé
 ❍ /password *:*  ᴅᴏɴɴᴇʀ ʟᴀ ʟᴏɴɢᴜᴇᴜʀ ᴅᴜ ᴍᴏᴛ ᴅᴇ ᴘᴀssᴇ ᴘᴏᴜʀ ʟᴇ ɢéɴéʀᴇʀ
 ❍ /uselessfact *:* Gᴇ́ɴᴇ́ʀᴇ ᴜɴ ғᴀɪᴛ ɪɴᴜᴛɪʟᴇ ᴀʟéᴀᴛᴏɪʀᴇ
"""
