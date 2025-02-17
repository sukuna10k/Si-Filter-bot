# Credit - @sd_bots

import os, wget
import shutil
import time
from datetime import datetime
from typing import Tuple
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message
from info import LOG_CHANNEL

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """run command in terminal"""
    args = cmd.split()
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )

async def convert_to_audio(vid_path):
    stark_cmd = f"ffmpeg -i {vid_path} -map 0:a sd.mp3"
    _, _, returncode, _ = await runcmd(stark_cmd)
    final_warner = "sd.mp3"
    if not os.path.exists(final_warner) or returncode != 0:
        return None
    return final_warner

@Client.on_message(filters.command(["convert", "audio"]))
async def shazam_(client, message):
    try:
        if not message.reply_to_message or not message.reply_to_message.video:
            return await message.reply_text("Répondez à une vidéo...")
        thumbnail = wget.download("https://telegra.ph/file/f4f20a3a7b15d588fcc2a.jpg")
        sd = await client.send_message(LOG_CHANNEL, text=f"#ᴠɪᴅ_ᴛᴏ_ᴀᴜᴅ\n\nʀᴇǫᴜᴇsᴛᴇᴅ ғʀᴏᴍ {message.from_user.mention}\n\nᴀᴜᴅɪᴏ: ❌")
        stime = time.time()
        msg = await message.reply_text("Conversion de la vidéo en audio...\n\nCela peut prendre du temps en fonction de la durée de la vidéo, veuillez patienter.")
        video_file = await message.reply_to_message.download()
        music_file = await convert_to_audio(video_file)
        if music_file is None:
            return await msg.edit("Échec de la conversion de la vidéo en audio.")
        etime = time.time()
        t_k = round(etime - stime)
        await message.reply_audio(music_file, thumb=thumbnail)
        await sd.edit(f"#ᴠɪᴅ_ᴛᴏ_ᴀᴜᴅ\nʀᴇǫᴜᴇsᴛᴇᴅ ғʀᴏᴍ {message.from_user.mention}\n\nᴀᴜᴅɪᴏ: ✅\nTemps de conversion vidéo en audio : {t_k}")
        t_taken = await message.reply_text(f"<code>{t_k} secondes pour convertir cette vidéo en audio...</code>")
        await asyncio.sleep(10)
        await t_taken.delete()
        await msg.delete()
        os.remove(video_file)
        os.remove(music_file)
    except Exception as e:
        await message.reply_text(f"Erreur : {e}")
