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
        'name': 'Chain Cube 2048',
        'appToken': 'd1690a07-3780-4068-810f-9b5bbf2931b2',
        'promoId': 'b4170868-cef0-424f-8eb9-be0622e8e8e3',
        'timing': 25000 / 1000,
        'attempts': 20,
    },
    2: {
        'name': 'Train Miner',
        'appToken': '82647f43-3f87-402d-88dd-09a90025313f',
        'promoId': 'c4480ac7-e178-4973-8061-9ed5b2e17954',
        'timing': 20000 / 1000,
        'attempts': 15,
    },
    3: {
        'name': 'Merge Away',
        'appToken': '8d1cc2ad-e097-4b86-90ef-7a27e19fb833',
        'promoId': 'dc128d28-c45b-411c-98ff-ac7726fbaea4',
        'timing': 20000 / 1000,
        'attempts': 25,
    },
    4: {
        'name': 'Twerk Race 3D',
        'appToken': '61308365-9d16-4040-8bb0-2f4a4c69074c',
        'promoId': '61308365-9d16-4040-8bb0-2f4a4c69074c',
        'timing': 20000 / 1000,
        'attempts': 20,
    },
    5: {
        'name': 'Polysphere',
        'appToken': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71',
        'promoId': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71',
        'timing': 20000 / 1000,
        'attempts': 20,
    },
    6: {
        'name': 'Mow and Trim',
        'appToken': 'ef319a80-949a-492e-8ee0-424fb5fc20a6',
        'promoId': 'ef319a80-949a-492e-8ee0-424fb5fc20a6',
        'timing': 20000 / 1000,
        'attempts': 20,
    },
    7: {
        'name': 'Tile Trio',
        'appToken': 'e68b39d2-4880-4a31-b3aa-0393e7df10c7',
        'promoId': 'e68b39d2-4880-4a31-b3aa-0393e7df10c7',
        'timing': 20000 / 1000,
        'attempts': 20,
    },
    8: {
        'name': 'Zoopolis',
        'appToken': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b',
        'promoId': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b',
        'timing': 20000 / 1000,
        'attempts': 20,
    },
    9: {
        'name': 'Fluff Crusade',
        'appToken': '112887b0-a8af-4eb2-ac63-d82df78283d9',
        'promoId': '112887b0-a8af-4eb2-ac63-d82df78283d9',
        'timing': 30000 / 1000,
        'attempts': 20,
    },
    10: {
        'name': 'Stone Age',
        'appToken': '04ebd6de-69b7-43d1-9c4b-04a6ca3305af',
        'promoId': '04ebd6de-69b7-43d1-9c4b-04a6ca3305af',
        'timing': 20000 / 1000,
        'attempts': 20,
    },
   11: {
        'name': 'Bouncemasters',
        'appToken': 'bc72d3b9-8e91-4884-9c33-f72482f0db37',
        'promoId': 'bc72d3b9-8e91-4884-9c33-f72482f0db37',
        'timing': 20000 / 1000,
        'attempts': 20,
    },
    12: {
        'name': 'Hide Ball',
        'appToken': '4bf4966c-4d22-439b-8ff2-dc5ebca1a600',
        'promoId': '4bf4966c-4d22-439b-8ff2-dc5ebca1a600',
        'timing': 40000 / 1000,
        'attempts': 20,
    },
    13: {
        'name': 'Pin Out Master',
        'appToken': 'd2378baf-d617-417a-9d99-d685824335f0',
        'promoId': 'd2378baf-d617-417a-9d99-d685824335f0',
        'timing': 30000 / 1000,
        'attempts': 20,
    },
    14: {
        'name': 'Count Masters',
        'appToken': '4bdc17da-2601-449b-948e-f8c7bd376553',
        'promoId': '4bdc17da-2601-449b-948e-f8c7bd376553',
        'timing': 30000 / 1000,
        'attempts': 20,
    },
    15: {
        'name': 'Infected Frontier',
        'appToken': 'eb518c4b-e448-4065-9d33-06f3039f0fcb',
        'promoId': 'eb518c4b-e448-4065-9d33-06f3039f0fcb',
        'timing': 30000 / 1000,
        'attempts': 20,
    },
    16: {
        'name': 'Among Waterr',
        'appToken': 'daab8f83-8ea2-4ad0-8dd5-d33363129640',
        'promoId': 'daab8f83-8ea2-4ad0-8dd5-d33363129640',
        'timing': 30000 / 1000,
        'attempts': 20,
    },
    17: {
        'name': 'Factory World',
        'appToken': 'd02fc404-8985-4305-87d8-32bd4e66bb16',
        'promoId': 'd02fc404-8985-4305-87d8-32bd4e66bb16',
        'timing': 30000 / 1000,
        'attempts': 20,
    },
}


async def load_proxies(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                proxies = [line.strip() for line in file if line.strip()]
                random.shuffle(proxies)  # Shuffle proxies to ensure randomness
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


async def login(client_id, app_token, proxies, retries=5):
    for attempt in range(retries):
        proxy = random.choice(proxies) if proxies else None
        async with httpx.AsyncClient(proxies=proxy) as client:
            try:
                logger.info(f"Attempting to log in with client ID: {client_id} (Attempt {attempt + 1}/{retries})")
                response = await client.post(
                    'https://api.gamepromo.io/promo/login-client',
                    json={'appToken': app_token, 'clientId': client_id, 'clientOrigin': 'deviceid'}
                )
                response.raise_for_status()
                data = response.json()
                logger.info(f"Login successful for client ID: {client_id}")
                return data['clientToken']
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to login (attempt {attempt + 1}/{retries}): {e.response.json()}")
            except Exception as e:
                logger.error(f"Unexpected error during login (attempt {attempt + 1}/{retries}): {e}")
        await asyncio.sleep(2)  # Delay before retrying
    logger.error("Maximum login attempts reached. Returning None.")
    return None


async def emulate_progress(client_token, promo_id, proxies):
    proxy = random.choice(proxies) if proxies else None
    logger.info(f"Emulating progress for promo ID: {promo_id}")
    async with httpx.AsyncClient(proxies=proxy) as client:
        response = await client.post(
            'https://api.gamepromo.io/promo/register-event',
            headers={'Authorization': f'Bearer {client_token}'},
            json={'promoId': promo_id, 'eventId': str(uuid.uuid4()), 'eventOrigin': 'undefined'}
        )
        response.raise_for_status()
        data = response.json()
        return data['hasCode']


async def generate_key(client_token, promo_id, proxies):
    proxy = random.choice(proxies) if proxies else None
    logger.info(f"Generating key for promo ID: {promo_id}")
    async with httpx.AsyncClient(proxies=proxy) as client:
        response = await client.post(
            'https://api.gamepromo.io/promo/create-code',
            headers={'Authorization': f'Bearer {client_token}'},
            json={'promoId': promo_id}
        )
        response.raise_for_status()
        data = response.json()
        return data['promoCode']


async def generate_key_process(app_token, promo_id, proxies, timing, attempts):
    client_id = await generate_client_id()
    logger.info(f"Generated client ID: {client_id}")
    client_token = await login(client_id, app_token, proxies)
    if not client_token:
        logger.error(f"Failed to generate client token for client ID: {client_id}")
        return None

    for i in range(attempts):
        logger.info(f"Emulating progress event {i + 1}/{attempts} for client ID: {client_id}")
        await asyncio.sleep(timing * (random.random() / 3 + 1))
        try:
            has_code = await emulate_progress(client_token, promo_id, proxies)
        except httpx.HTTPStatusError:
            logger.warning(f"Event {i + 1}/{attempts} failed for client ID: {client_id}")
            continue

        if has_code:
            logger.info(f"Progress event triggered key generation for client ID: {client_id}")
            break

    try:
        key = await generate_key(client_token, promo_id, proxies)
        logger.info(f"Generated key: {key} for client ID: {client_id}")
        return key
    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to generate key: {e.response.json()}")
        return None


async def spinner_task():
    spinner = ["|", "/", "-", "\\"]
    idx = 0
    while True:
        sys.stdout.write(f"\rWorking... {spinner[idx]}")
        sys.stdout.flush()
        idx = (idx + 1) % len(spinner)
        await asyncio.sleep(0.1)


async def main(game_choice, key_count, proxies):
    game = games[game_choice]
    logger.info(f"Starting key generation for {game['name']}")

    spinner = asyncio.create_task(spinner_task())  # Start the spinner task

    tasks = [
        generate_key_process(
            game['appToken'],
            game['promoId'],
            proxies,
            game['timing'],
            game['attempts']
        )
        for _ in range(key_count)
    ]
    keys = await asyncio.gather(*tasks)

    spinner.cancel()  # Stop the spinner task
    sys.stdout.write("\r")  # Clear the spinner line

    logger.info(f"Key generation completed for {game['name']}")
    return [key for key in keys if key], game['name']


if __name__ == "__main__":
    print("Select a game:")
    for key, value in games.items():
        print(f"{key}: {value['name']}")
    game_choice = int(input("Enter the game number: "))
    key_count = int(input("Enter the number of keys to generate: "))
    proxy_file = input("Enter the proxy file path (leave empty to use 'proxy.txt'): ") or 'proxy.txt'

    proxies = asyncio.run(load_proxies(proxy_file))

    logger.info(
        f"Generating {key_count} key(s) for {games[game_choice]['name']} using proxies from {proxy_file if proxies else 'no proxies'}")
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
