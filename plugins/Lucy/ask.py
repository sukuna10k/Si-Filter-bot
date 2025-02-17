# crédits @hyoshcoder

import requests
from HorridAPI import api 
from pyrogram import Client, filters

@Client.on_message(filters.command("ask"))
async def ask(client, message):    
    if len(message.command) < 2:
        return await message.reply_text("Veuillez fournir une requête !")
    
    query = " ".join(message.command[1:])
    thinking_message = await message.reply_text("<b>Veuillez patienter une seconde...</b>")
    try:        
        response = api.llama(query)        
        await thinking_message.edit(f"Hé {message.from_user.mention},\n\nRequête : {query}\n______________\nRésultat :\n{response}")

    except Exception as e:  
        # print(e)
        error_message = f"Hmm, quelque chose s'est mal passé : {str(e)}"[:100] + "...\n utilisez /bug commentaire"
        await thinking_message.edit(error_message)
