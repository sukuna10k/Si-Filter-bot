from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import *


async def get_fsub(bot, message):
    target_channel_id = AUTH_CHANNEL  # Votre ID de chaîne
    user_id = message.from_user.id
    try:
        await bot.get_chat_member(target_channel_id, user_id)
    except UserNotParticipant:
        channel_link = (await bot.get_chat(target_channel_id)).invite_link
        join_button = InlineKeyboardButton("Rejoignez mes mises à jour", url=channel_link)
        keyboard = [[join_button]]
        await message.reply(
            f"<b>Cher utilisateur {message.from_user.mention}!\n\nVeuillez rejoindre notre chaîne de mises à jour pour m'utiliser ! 😊\n\nEn raison de la surcharge du serveur, seuls les abonnés de notre chaîne peuvent utiliser ce bot !</b>",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return False
    else:
        return True
