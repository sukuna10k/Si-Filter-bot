import httpx, base64
from pyrogram import Client, filters


@Client.on_message(filters.command("upscale"))
async def upscale_image(client, message):
    try:
        # Vérifiez si le message auquel on répond contient une photo
        if message.reply_to_message and message.reply_to_message.photo:
            # Envoyez un message indiquant que l'agrandissement est en cours
            progress_msg = await message.reply_text(
                "✦ Agrandissement de votre image, veuillez patienter..."
            )

          
            image = message.reply_to_message.photo.file_id
            file_path = await client.download_media(image)

            with open(file_path, "rb") as image_file:
                f = image_file.read()

            b = base64.b64encode(f).decode("utf-8")

            async with httpx.AsyncClient() as http_client:
                response = await http_client.post(
                    "https://api.qewertyy.me/upscale",
                    data={"image_data": b},
                    timeout=None,
                )

            # Enregistrez l'image agrandie
            upscaled_file_path = "upscaled_image.png"
            with open(upscaled_file_path, "wb") as output_file:
                output_file.write(response.content)

            # Supprimez le message de progression
            await progress_msg.delete()

            # Envoyez l'image agrandie en tant que fichier PNG
            await client.send_document(
                message.chat.id,
                document=upscaled_file_path,
                caption=f"✦ Généré par ➠ [Lucy](https://t.me/HokageMovie_bot)\n\n✦ Mise à jour ➠ [CodeFlix Bots](https://t.me/hyoshassistantbot)",
            )
        else:
            await message.reply_text("✦ Veuillez répondre à une image pour l'agrandir.")

    except Exception as e:
        print(f"✦ Échec de l'agrandissement de l'image ➛ {e}")
        await message.reply_text("✦ Échec de l'agrandissement de l'image. Veuillez réessayer plus tard.")
