import asyncio
import logging
from info import *
from pyrogram import Client
from util.config_parser import TokenParser
from . import multi_clients, work_loads, hyoshcoder


async def initialize_clients():
    multi_clients[0] = hyoshcoder
    work_loads[0] = 0
    tous_les_tokens = TokenParser().parse_from_env()
    if not tous_les_tokens:
        print("Aucun client supplémentaire trouvé, utilisation du client par défaut")
        return
    
    async def start_client(client_id, token):
        try:
            print(f"Démarrage - Client {client_id}")
            if client_id == len(tous_les_tokens):
                await asyncio.sleep(2)
                print("Cela prendra un certain temps, veuillez patienter...")
            client = await Client(
                name=str(client_id),
                api_id=API_ID,
                api_hash=API_HASH,
                bot_token=token,
                sleep_threshold=SLEEP_THRESHOLD,
                no_updates=True,
                in_memory=True
            ).start()
            work_loads[client_id] = 0
            return client_id, client
        except Exception:
            logging.error(f"Échec du démarrage du Client - {client_id} Erreur:", exc_info=True)
    
    clients = await asyncio.gather(*[start_client(i, token) for i, token in tous_les_tokens.items()])
    multi_clients.update(dict(clients))
    if len(multi_clients) != 1:
        MULTI_CLIENT = True
        print("Mode Multi-Client Activé")
    else:
        print("Aucun client supplémentaire n'a été initialisé, utilisation du client par défaut")