from pyrogram import Client, filters
from pyrogram.types import Message
import traceback
import sys
import io

@Client.on_message(filters.command("python"))
async def execute_python_code(client, message: Message):
    if len(message.command) < 2:
        await message.reply("❌ Veuillez entrer votre code Python après la commande. Exemple : `/python print('Hello, World!')`")
        return

    python_code = " ".join(message.command[1:])

    output_buffer = io.StringIO()
    sys.stdout = output_buffer

    try:
        exec(python_code, {"__builtins__": __builtins__}, {})
        output = output_buffer.getvalue().strip()

        result_message = output if output else "Aucun retour"

        await message.reply(f"✅ Code exécuté avec succès. Résultat :\n{result_message}")

    except Exception as e:
        traceback_str = traceback.format_exc()

        await message.reply(f"❌ Une erreur est survenue. Détails :\n{traceback_str}")

    finally:
        sys.stdout = sys.__stdout__ 
        output_buffer.close()  
