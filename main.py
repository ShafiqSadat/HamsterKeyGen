import asyncio
import os
import sys
import httpx
import random
import time
import uuid
from loguru import logger

# Disable logging for httpx
httpx_log = logger.bind(name="httpx").level("WARNING")
logger.remove()
logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
                                   " | <level>{level: <8}</level>"
                                   " | <cyan><b>{line}</b></cyan>"
                                   " - <white><b>{message}</b></white>")
logger = logger.opt(colors=True)

games = {
    1: {
        'name': 'Riding Extreme 3D',
        'appToken': 'd28721be-fd2d-4b45-869e-9f253b554e50',
        'promoId': '43e35910-c168-4634-ad4f-52fd764a843f',
    },
    2: {
        'name': 'Chain Cube 2048',
        'appToken': 'd1690a07-3780-4068-810f-9b5bbf2931b2',
        'promoId': 'b4170868-cef0-424f-8eb9-be0622e8e8e3',
    },
    3: {
        'name': 'My Clone Army',
        'appToken': '74ee0b5b-775e-4bee-974f-63e7f4d5bacb',
        'promoId': 'fe693b26-b342-4159-8808-15e3ff7f8767',
    },
    4: {
        'name': 'Train Miner',
        'appToken': '82647f43-3f87-402d-88dd-09a90025313f',
        'promoId': 'c4480ac7-e178-4973-8061-9ed5b2e17954',
    }
}

EVENTS_DELAY = 20000 / 1000  # converting milliseconds to seconds

async def load_proxies(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                proxies = [line.strip() for line in file if line.strip()]
                return proxies
        else:
            logger.info(f"Proxy file {file_path} not found. No proxies will be used.")
            return []
    except Exception as e:
        logger.error(f"Error reading proxy file {file_path}: {e}")
        return []

async def generate_client_id():
    timestamp = int(time.time() * 1000)
    random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(19))
    return f"{timestamp}-{random_numbers}"

async def login(client_id, app_token, proxy=None):
    async with httpx.AsyncClient(proxies=proxy) as client:
        response = await client.post(
            'https://api.gamepromo.io/promo/login-client',
            json={'appToken': app_token, 'clientId': client_id, 'clientOrigin': 'deviceid'}
        )
        response.raise_for_status()
        data = response.json()
        return data['clientToken']

async def emulate_progress(client_token, promo_id, proxy=None):
    async with httpx.AsyncClient(proxies=proxy) as client:
        response = await client.post(
            'https://api.gamepromo.io/promo/register-event',
            headers={'Authorization': f'Bearer {client_token}'},
            json={'promoId': promo_id, 'eventId': str(uuid.uuid4()), 'eventOrigin': 'undefined'}
        )
        response.raise_for_status()
        data = response.json()
        return data['hasCode']

async def generate_key(client_token, promo_id, proxy=None):
    async with httpx.AsyncClient(proxies=proxy) as client:
        response = await client.post(
            'https://api.gamepromo.io/promo/create-code',
            headers={'Authorization': f'Bearer {client_token}'},
            json={'promoId': promo_id}
        )
        response.raise_for_status()
        data = response.json()
        return data['promoCode']

async def generate_key_process(app_token, promo_id, proxies):
    client_id = await generate_client_id()
    proxy = random.choice(proxies) if proxies else None
    try:
        client_token = await login(client_id, app_token, proxy)
    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to login: {e.response.json()}")
        return None

    for _ in range(11):
        await asyncio.sleep(EVENTS_DELAY * (random.random() / 3 + 1))
        proxy = random.choice(proxies) if proxies else None
        try:
            has_code = await emulate_progress(client_token, promo_id, proxy)
        except httpx.HTTPStatusError as e:
            continue

        if has_code:
            break

    proxy = random.choice(proxies) if proxies else None
    try:
        key = await generate_key(client_token, promo_id, proxy)
        return key
    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to generate key: {e.response.json()}")
        return None

async def main(game_choice, key_count, proxies):
    game = games[game_choice]
    tasks = [generate_key_process(game['appToken'], game['promoId'], proxies) for _ in range(key_count)]
    keys = await asyncio.gather(*tasks)
    return [key for key in keys if key], game['name']

if __name__ == "__main__":
    print("Select a game:")
    for key, value in games.items():
        print(f"{key}: {value['name']}")
    game_choice = int(input("Enter the game number: "))
    key_count = int(input("Enter the number of keys to generate: "))
    proxy_file = input("Enter the proxy file path (leave empty to use 'proxy.txt'): ") or 'proxy.txt'

    proxies = asyncio.run(load_proxies(proxy_file))

    logger.info(f"Generating {key_count} key(s) for {games[game_choice]['name']} using proxies from {proxy_file if proxies else 'no proxies'}")
    keys, game_name = asyncio.run(main(game_choice, key_count, proxies))
    if keys:
        file_name = f"{game_name.replace(' ', '_').lower()}_keys.txt"
        logger.success(f"Generated Key(s) were successfully saved to {file_name}.")
        with open(file_name, 'a') as file:  # Open the file in append mode
            for key in keys:
                formatted_key = f"{key}"
                logger.success(formatted_key)
                file.write(f"{formatted_key}\n")
    else:
        logger.error("No keys were generated.")

    input("Press enter to exit")
