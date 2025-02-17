import requests
from info import BOT_NAME, BOT_USERNAME
import time
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import Client, filters

@Client.on_message(filters.command(["pass"]))
async def passwordgen(bot, message):
    
    try:
        
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            return await message.reply_text(
            "Exemple:**\n\n`/password <longueur>`")
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://mukesh-api.vercel.app/password?num={a}') 
            x=response.json()["results"]
            
            await message.reply_text(f"Voici votre mot de passe : ` {x}`", parse_mode=ParseMode.MARKDOWN)     
    except Exception as e:
        await message.reply_text(f"**Erreur : {e} ")
@Client.on_message(filters.command(["morseencode"]))
async def morse_en(bot, message):
    
    try:
        
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            return await message.reply_text(
            "Exemple:**\n\n`/morseencode <requête>`")
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://mukesh-api.vercel.app/morse/encode?query={a}') 
            x=response.json()["results"]
            
            await message.reply_text(f"`{x}`", parse_mode=ParseMode.MARKDOWN)     
    except Exception as e:
        await message.reply_text(f"**Erreur : {e} ")
@Client.on_message(filters.command("morsedecode"))
async def morse_de(bot, message):
    
    try:
        
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            return await message.reply_text(
            "Exemple:**\n\n`/morsedecode <requête>`")
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://mukesh-api.vercel.app/morse/decode?query={a}') 
            x=response.json()["results"]
            
            await message.reply_text(f"`{x}`", parse_mode=ParseMode.MARKDOWN)     
    except Exception as e:
        await message.reply_text(f"**Erreur : {e} ")
@Client.on_message(filters.command(["encode"]))
async def base_en(bot, message):
    
    try:
        
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            return await message.reply_text(
            "Exemple:**\n\n`/encode <requête>`")
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://mukesh-api.vercel.app/base/encode?query={a}') 
            x=response.json()["results"]
            
            await message.reply_text(f"` {x}`", parse_mode=ParseMode.MARKDOWN)     
    except Exception as e:
        await message.reply_text(f"**Erreur : {e} ")
@Client.on_message(filters.command(["decode"]))
async def base_de(bot, message):
    
    try:
        
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            return await message.reply_text(
            "Exemple:**\n\n`/decode <requête>`")
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://mukesh-api.vercel.app/base/decode?query={a}') 
            x=response.json()["results"]
            
            await message.reply_text(f" `{x}`", parse_mode=ParseMode.MARKDOWN)     
    except Exception as e:
        await message.reply_text(f"**Erreur : {e} ")                                
