from traceback import format_exc
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from search_engine_parser.core.engines.google import Search as GoogleSearch
from search_engine_parser.core.engines.stackoverflow import Search as StackSearch
from search_engine_parser.core.exceptions import NoResultsFound, NoResultsOrTrafficError
from pyrogram import Client, filters

gsearch = GoogleSearch()
stsearch = StackSearch()

def ikb(rows=None, back=False, todo="start_back"):
    """
    rows = passez les lignes
    back - si vous voulez ajouter un bouton de retour
    todo - données de callback du bouton de retour
    """
    if rows is None:
        rows = []
    lines = []
    try:
        for row in rows:
            line = []
            for button in row:
                btn_text = button.split(".")[1].capitalize()
                button = btn(btn_text, button)  
                line.append(button)
            lines.append(line)
    except AttributeError:
        for row in rows:
            line = []
            for button in row:
                button = btn(*button)  
                line.append(button)
            lines.append(line)
    except TypeError:
        # code pour gérer cette erreur
        line = []
        for button in rows:
            button = btn(*button)  # InlineKeyboardButton
            line.append(button)
        lines.append(line)
    if back: 
        back_btn = [(btn("Retour", todo))]
        lines.append(back_btn)
    return InlineKeyboardMarkup(inline_keyboard=lines)


def btn(text, value, type="callback_data"):
    return InlineKeyboardButton(text, **{type: value})

@Client.on_message(filters.command('google'))
async def search_(Client: Client, msg: Message):
    split = msg.text.split(None, 1)
    if len(split) == 1:
        return await msg.reply_text("**Donnez une requête pour effectuer une recherche**")
    to_del = await msg.reply_text("**Recherche sur Google en cours...**")
    query = split[1]
    try:
        result = await gsearch.async_search(query)
        keyboard = ikb(
            [
                [
                    (
                        f"{result[0]['titles']}",
                        f"{result[0]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[1]['titles']}",
                        f"{result[1]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[2]['titles']}",
                        f"{result[2]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[3]['titles']}",
                        f"{result[3]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[4]['titles']}",
                        f"{result[4]['links']}",
                        "url",
                    ),
                ],
            ]
        )

        txt = f"**Voici les résultats pour la requête : {query.title()}**"
        await to_del.delete()
        await msg.reply_text(txt, reply_markup=keyboard)
        return
    except NoResultsFound:
        await to_del.delete()
        await msg.reply_text("**Aucun résultat trouvé correspondant à votre requête**")
        return
    except NoResultsOrTrafficError:
        await to_del.delete()
        await msg.reply_text("**Aucun résultat trouvé en raison de trop de trafic**")
        return
    except Exception as e:
        await to_del.delete()
        await msg.reply_text(f"**Quelque chose a mal tourné :\nSignalez-le à** @iam_daxx")
        print(f"erreur : {e}")
        return

@Client.on_message(filters.command('stack'))
async def stack_search_(Client: Client, msg: Message):
    split = msg.text.split(None, 1)
    if len(split) == 1:
        return await msg.reply_text("**Donnez une requête pour effectuer une recherche**")
    to_del = await msg.reply_text("**Recherche sur StackOverflow en cours...**")
    query = split[1]
    try:
        result = await stsearch.async_search(query)
        keyboard = ikb(
            [
                [
                    (
                        f"{result[0]['titles']}",
                        f"{result[0]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[1]['titles']}",
                        f"{result[1]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[2]['titles']}",
                        f"{result[2]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[3]['titles']}",
                        f"{result[3]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[4]['titles']}",
                        f"{result[4]['links']}",
                        "url",
                    ),
                ],
            ]
        )

        txt = f"**Voici les résultats pour la requête : {query.title()}**"
        await to_del.delete()
        await msg.reply_text(txt, reply_markup=keyboard)
        return
    except NoResultsFound:
        await to_del.delete()
        await msg.reply_text("**Aucun résultat trouvé correspondant à votre requête**")
        return
    except NoResultsOrTrafficError:
        await to_del.delete()
        await msg.reply_text("**Aucun résultat trouvé en raison de trop de trafic**")
        return
    except Exception as e:
        await to_del.delete()
        await msg.reply_text(f"**Quelque chose a mal tourné :\nSignalez-le à** @DevsOops")
        print(f"erreur : {e}")
        return
