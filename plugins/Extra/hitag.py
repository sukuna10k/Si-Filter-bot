import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions

spam_chats = []

EMOJI = [ "🦋🦋🦋🦋🦋",
          "🧚🌸🧋🍬🫖",
          "🥀🌷🌹🌺💐",
          "🌸🌿💮🌱🌵",
          "❤️💚💙💜🖤",
          "💓💕💞💗💖",
          "🌸💐🌺🌹🦋",
          "🍔🦪🍛🍲🥗",
          "🍎🍓🍒🍑🌶️",
          "🧋🥤🧋🥛🍷",
          "🍬🍭🧁🎂🍡",
          "🍨🧉🍺☕🍻",
          "🥪🥧🍦🍥🍚",
          "🫖☕🍹🍷🥛",
          "☕🧃🍩🍦🍙",
          "🍁🌾💮🍂🌿",
          "🌨️🌥️⛈️🌩️🌧️",
          "🌷🏵️🌸🌺💐",
          "💮🌼🌻🍀🍁",
          "🧟🦸🦹🧙👸",
          "🧅🍠🥕🌽🥦",
          "🐷🐹🐭🐨🐻‍❄️",
          "🦋🐇🐀🐈🐈‍⬛",
          "🌼🌳🌲🌴🌵",
          "🥩🍋🍐🍈🍇",
          "🍴🍽️🔪🍶🥃",
          "🕌🏰🏩⛩️🏩",
          "🎉🎊🎈🎂🎀",
          "🪴🌵🌴🌳🌲",
          "🎄🎋🎍🎑🎎",
          "🦅🦜🕊️🦤🦢",
          "🦤🦩🦚🦃🦆",
          "🐬🦭🦈🐋🐳",
          "🐔🐟🐠🐡🦐",
          "🦩🦀🦑🐙🦪",
          "🐦🦂🕷️🕸️🐚",
          "🥪🍰🥧🍨🍨",
          " 🥬🍉🧁🧇",
        ]

TAGMES = [
    " **❅ Bébé, où es-tu ? 🤗** ",
    " **❅ Hé, tu dors ? Viens en ligne 😊** ",
    " **❅ Viens en vocal, on discute 😃** ",
    " **❅ Tu as mangé ou pas ? 🥲** ",
    " **❅ Comment va la famille ? 🥺** ",
    " **❅ Tu sais, tu me manques beaucoup 🤭** ",
    " **❅ Alors, raconte, comment ça va ? 🤨** ",
    " **❅ Trouve-moi aussi quelqu'un, s'il te plaît 🙂** ",
    " **❅ Comment tu t'appelles ? 🥲** ",
    " **❅ Tu as pris ton petit-déjeuner ? 😋** ",
    " **❅ Ajoute-moi dans ton groupe 😍** ",
    " **❅ Ton ami t'appelle 😅** ",
    " **❅ Veux-tu m'épouser ? 🤔** ",
    " **❅ Tu es déjà parti dormir ? 🙄** ",
    " **❅ Hé, quelqu'un peut allumer la clim ? 😕** ",
    " **❅ D'où viens-tu ? 🙃** ",
    " **❅ Bonjour à tous 😛** ",
    " **❅ Bébé, que fais-tu ? 🤔** ",
    " **❅ Est-ce que tu me connais ? ☺️** ",
    " **❅ Viens, on joue au Ludo 🤗** ",
    " **❅ On sort ce soir de 9 à 12... 😇** ",
    " **❅ Que fait ton père ? 🤭** ",
    " **❅ Viens bébé, on va manger des snacks 🥺** ",
    " **❅ Ne va pas seule au marché, on pourrait t'envier 😶** ",
    " **❅ Alors, comment va ton copain ? 🤔** ",
    " **❅ Bonjour 😜** ",
    " **❅ Tu peux faire quelque chose pour moi ? 🙂** ",
    " **❅ DJ, mets ma chanson 😪** ",
    " **❅ Ravi de te rencontrer ☺** ",
    " **❅ Mon bébé a bien mangé ? 🙊** ",
    " **❅ Comment vont tes études ? 😺** ",
    " **❅ Je suis tombé amoureux 🥲** ",
    " **❅ Qui est Nykaa...? 😅** ",
    " **❅ Prends une photo de moi 😅** ",
    " **❅ Raccroche, ta mère arrive ? 😆** ",
    " **❅ Quand vas-tu me présenter ta belle-sœur ? 😉** ",
    " **❅ Est-ce que tu m'aimes ? 💚** ",
    " **❅ Je t'aime beaucoup..! 👀** ",
    " **❅ Bébé, un bisou s'il te plaît..?? 🙉** ",
    " **❅ Veux-tu entendre une blague..? 😹** ",
    " **❅ Viens en vocal, j'ai quelque chose à te montrer 😻** ",
    " **❅ Utilises-tu Instagram..? 🙃** ",
    " **❅ Donne-moi ton numéro WhatsApp..? 😕** ",
    " **❅ Présente-moi ton amie..? 🙃** ",
    " **❅ Si tu as fini ton travail, viens en ligne 🙃** ",
    " **❅ D'où viens-tu ? 😊** ",
    " **❅ Je te libère de mon cœur 🥺** ",
    " **❅ Fais-moi une faveur, ajoute des membres au groupe.. ♥️** ",
    " **❅ Je suis en colère contre toi 😠** ",
    " **❅ Comment va ta famille..? ❤** ",
    " **❅ Qu'est-ce qui s'est passé..? 🤔** ",
    " **❅ Tu me manques beaucoup 😒** ",
    " **❅ Tu m'as oublié 😏** ",
    " **❅ Pourquoi tu m'as menti ? 🤐** ",
    " **❅ Ne sois pas trop fière, mange bien et deviens forte 😒** ",
    " **❅ À qui montres-tu cet attitude ? 😮** ",
    " **❅ Hello, occupée où ? 👀** ",
    " **❅ Je suis heureux de t'avoir comme ami 🙈** ",
    " **❅ Je me sens triste aujourd'hui ☹️** ",
    " **❅ Parle-moi un peu 🥺** ",
    " **❅ Qu'as-tu cuisiné aujourd'hui ? 👀** ",
    " **❅ Quoi de neuf ? 🙂** ",
    " **❅ Pourquoi tu ne m'envoies pas de message..? 🥺** ",
    " **❅ Je suis innocent(e) non ? 🥺** ",
    " **❅ C'était bien hier, non ? 😅** ",
    " **❅ Où étais-tu occupé hier ? 😕** ",
    " **❅ Es-tu en couple..? 👀** ",
    " **❅ Tu es toujours si calme 😼** ",
    " **❅ Sais-tu chanter ? 😸** ",
    " **❅ Viens, on part en voyage..? 🙈** ",
    " **❅ Sois toujours heureux 🤞** ",
    " **❅ Peut-on être amis..? 🥰** ",
    " **❅ Es-tu marié(e)..? 🥺** ",
    " **❅ Où étais-tu ces derniers jours ? 🥲** ",
    " **❅ Célibataire ou en couple ? 😉** ",
    " **❅ Viens, faisons la fête 🥳** ",
    " **❅ Il y a un lien dans ma bio, rejoins-nous 🧐** ",
    " **❅ Je ne t'aime pas 🥺** ",
    " **❅ Viens ici @THE_FRIENDZ, on va s'amuser 🤭** ",
    " **❅ Oublie-moi 😊** ",
    " **❅ Fais-moi tien, mon amour 🥺** ",
    " **❅ Rejoins mon groupe aussi 🤗** ",
    " **❅ J'ai nommé mon cœur d'après toi 😗** ",
    " **❅ Où sont passés tous tes amis ? 🥺** ",
    " **❅ Mon adorable propriétaire @Nykaa_update 🥰** ",
    " **❅ À qui penses-tu, chéri ? 😜** ",
    " **❅ Bonne nuit, il est tard 🥰** ",
]

VC_TAG = [
    "**❅ Si vous ne faites pas un pas en avant, vous resterez au même endroit.**",
    "**❅ La vie est difficile mais pas impossible.**",
    "**❅ La vie est trop courte pour se disputer et se battre.**",
    "**❅ N'attendez pas le moment parfait, prenez un moment et rendez-le parfait.**",
    "**❅ Le silence est la meilleure réponse pour quelqu'un qui ne valorise pas vos mots.**",
    "**❅ Chaque nouveau jour est une chance de changer votre vie.**",
    "**❅ Pour changer votre vie, vous devez changer vos priorités.**",
    "**❅ La vie est un voyage, pas une course.**",
    "**❅ Souriez et ne vous inquiétez pas, la vie est incroyable.**",
    "**❅ Ne vous comparez pas aux autres, si vous le faites, vous vous insultez vous-même.**",
    "**❅ Je suis en train de devenir la meilleure version de moi-même.**",
    "**❅ La vie est comme de la glace, profitez-en avant qu'elle ne fonde.**",
    "**❅ Soyez libre comme un oiseau.**",
    "**❅ Personne ne viendra vous sauver. Cette vie est entièrement votre responsabilité.**",
    "**❅ La vie vous offre toujours une seconde chance. Cela s'appelle demain.**",
    "**❅ La vie commence à la fin de votre zone de confort.**",
    "**❅ Toutes les choses qui vous blessent vous enseignent en réalité.**",
    "**❅ La vie est comme un appareil photo. Affrontez-la avec un sourire.**",
    "**❅ La vie, c'est 10 % ce qui vous arrive et 90 % comment vous y répondez.**",
    "**❅ La vie n'est pas une tâche facile.**",
    "**❅ La vie est une merveilleuse aventure.**",
    "**❅ La vie commence de l'autre côté du désespoir.**",
    "**❅ La vie n'est pas un problème à résoudre mais une réalité à expérimenter.**"
]


@Client.on_message(filters.command(["hitag"], prefixes=["/", "@", "#"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ Cette commande est réservée aux groupes.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ Vous n'êtes pas administrateur, seul un administrateur peut mentionner les membres.")

    if message.reply_to_message and message.text:
        return await message.reply("/hitag bonjour, écrivez comme ceci / répondez à un message la prochaine fois pour mentionner...")
    elif message.text:
        mode = "texte_sur_commande"
        msg = message.text
    elif message.reply_to_message:
        mode = "texte_sur_réponse"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("/hitag bonjour, écrivez comme ceci / répondez à un message la prochaine fois pour mentionner...")
    else:
        return await message.reply("/hitag bonjour, écrivez comme ceci / répondez à un message la prochaine fois pour mentionner...")

    if chat_id in spam_chats:
        return await message.reply("๏ Veuillez d'abord arrêter le processus de mention...")
    
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            if mode == "texte_sur_commande":
                txt = f"{usrtxt} {random.choice(TAGMES)}"
                await client.send_message(chat_id, txt)
            elif mode == "texte_sur_réponse":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@Client.on_message(filters.command(["lifetag"], prefixes=["/", "@", "#"]))
async def mention_allvc(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ Cette commande est réservée aux groupes.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ Vous n'êtes pas administrateur, seul un administrateur peut mentionner les membres.")

    if chat_id in spam_chats:
        return await message.reply("๏ Veuillez d'abord arrêter le processus de mention...")
    
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            txt = f"{usrtxt} {random.choice(VC_TAG)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@Client.on_message(filters.command(["cancel", "histop", "lifestop"]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("๏ Actuellement, je ne suis pas en train de mentionner, bébé.")
    
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ Vous n'êtes pas administrateur, seul un administrateur peut arrêter la mention.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("๏ Le processus de mention est arrêté.")
