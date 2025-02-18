from pyrogram import Client, filters
from info import LOG_CHANNEL
from SafoneAPI import SafoneAPI

safone = SafoneAPI()

@Client.on_message(filters.command(["bin"], [".", "!", "/"]))
async def check_bin(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "**Sᴇɴsᴇɪ, ᴠᴇᴜɪʟʟᴇᴢ ᴍᴇ ᴅᴏɴɴᴇʀ ᴜɴᴇ ʀᴇǫᴜêᴛᴇ ʙɪɴ ɴᴜᴍéʀɪǫᴜᴇ.**"
        )
    try:
        await message.delete()
    except:
        pass
    aux = await message.reply_text("<b>Aᴀʜ, ᴀᴛᴛᴇɴᴅᴇᴢ, ᴅᴏɴɴᴇᴢ-ᴍᴏɪ ᴜɴ �ᴇᴜ ᴘᴇᴜ ᴅᴇ ᴛᴇᴍᴘs...</b>")
    bin = message.split(None, 1)[1]
    await client.send_message(LOG_CHANNEL, text=f"#bin_check\nDemandé par : {message.from_user.mention}\nʟᴀ ᴅᴇᴍᴀɴᴅᴇ ᴇsᴛ {bin}")
    if len(bin) < 6:
        return await aux.edit("<b>Oᴏᴘs, ᴍᴏɴ ᴀᴍɪ, ғᴏʀᴍᴀᴛ ɪɴᴄᴏʀʀᴇᴄᴛ. Vᴇᴜɪʟʟᴇᴢ ᴍᴇ ᴅᴏɴɴᴇʀ ᴜɴ ʙɪɴ ᴠᴀʟɪᴅᴇ.</b>")
    try:
        resp = await safone.bininfo(bin)
        await aux.edit(f"""
<b> 𝗕𝗜𝗡 𝗩𝗔𝗟𝗜𝗗𝗘 ✅</b>
<b>┏━◆</b>
<b>┣〖🏦 Bᴀɴǫᴜᴇ</b> ⇾<tt>{resp.bank}</tt>
<b>┣〖💳 Bɪɴ</b> ⇾<tt>{resp.bin}</tt>
<b>┣〖🏡 Pᴀʏs</b> ⇾<tt>{resp.country}</tt>
<b>┣〖🇮🇳 Dʀᴀᴘᴇᴀᴜ</b> ⇾<tt>{resp.flag}</tt>
<b>┣〖🧿 Iᴅᴇɴᴛɪғɪᴀɴᴛ Iᴅᴇɴᴛɪғɪᴀɴᴛ</b> ⇾<tt>{resp.iso}</tt>
<b>┣〖⏳ Nɪᴠᴇᴀᴜ</b> ⇾<tt>{resp.level}</tt>
<b>┣〖🔴 Pʀéᴘᴀʏé</b> ⇾<tt>{resp.prepaid}</tt>
<b>┣〖🆔 Tʏᴘᴇ</b> ⇾<tt>{resp.type}</tt>
<b>┣〖ℹ️ Fᴏᴜʀɴɪssᴇᴜʀ</b> ⇾<tt>{resp.vendor}</tt>
<b>┗━━━◆</b>
"""
        )
    except:
        return await aux.edit("**🚫 Bɪɴ ɴᴏɴ ʀᴇᴄᴏɴɴᴜ, ᴠᴇᴜɪʟʟᴇᴢ ᴇɴᴛʀᴇʀ �ɴ ʙɪɴ ᴠᴀʟɪᴅᴇ.**")