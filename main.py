import asyncio
import httpx
import random
import time
import uuid

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


async def generate_client_id():
    timestamp = int(time.time() * 1000)
    random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(19))
    return f"{timestamp}-{random_numbers}"


async def login(client_id, app_token):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://api.gamepromo.io/promo/login-client',
            json={'appToken': app_token, 'clientId': client_id, 'clientOrigin': 'deviceid'}
        )
        response.raise_for_status()
        data = response.json()
        return data['clientToken']


async def emulate_progress(client_token, promo_id):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://api.gamepromo.io/promo/register-event',
            headers={'Authorization': f'Bearer {client_token}'},
            json={'promoId': promo_id, 'eventId': str(uuid.uuid4()), 'eventOrigin': 'undefined'}
        )
        response.raise_for_status()
        data = response.json()
        return data['hasCode']


async def generate_key(client_token, promo_id):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://api.gamepromo.io/promo/create-code',
            headers={'Authorization': f'Bearer {client_token}'},
            json={'promoId': promo_id}
        )
        response.raise_for_status()
        data = response.json()
        return data['promoCode']


async def generate_key_process(app_token, promo_id):
    client_id = await generate_client_id()
    try:
        client_token = await login(client_id, app_token)
    except httpx.HTTPStatusError as e:
        print(f"Failed to login: {e.response.json().get('message', 'Unknown error')}")
        return None

    for _ in range(11):
        await asyncio.sleep(EVENTS_DELAY * (random.random() / 3 + 1))
        try:
            has_code = await emulate_progress(client_token, promo_id)
        except httpx.HTTPStatusError as e:
            continue

        if has_code:
            break

    try:
        key = await generate_key(client_token, promo_id)
        return key
    except httpx.HTTPStatusError as e:
        print(f"Failed to generate key: {e.response.json().get('message', 'Unknown error')}")
        return None


async def main(game_choice, key_count):
    game = games[game_choice]
    tasks = [generate_key_process(game['appToken'], game['promoId']) for _ in range(key_count)]
    keys = await asyncio.gather(*tasks)
    return [key for key in keys if key]


if __name__ == "__main__":
    print("Select a game:")
    for key, value in games.items():
        print(f"{key}: {value['name']}")
    game_choice = int(input("Enter the game number: "))
    key_count = int(input("Enter the number of keys to generate: "))

    keys = asyncio.run(main(game_choice, key_count))
    if keys:
        print("Generated Keys:")
        for key in keys:
            print(key)
    else:
        print("No keys were generated.")
