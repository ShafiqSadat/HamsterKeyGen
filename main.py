import asyncio
import httpx
import random
import time
import uuid

APP_TOKEN = 'd28721be-fd2d-4b45-869e-9f253b554e50'
PROMO_ID = '43e35910-c168-4634-ad4f-52fd764a843f'
EVENTS_DELAY = 20000 / 1000  # converting milliseconds to seconds

async def generate_client_id():
    timestamp = int(time.time() * 1000)
    random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(19))
    return f"{timestamp}-{random_numbers}"

async def login(client_id):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://api.gamepromo.io/promo/login-client',
            json={'appToken': APP_TOKEN, 'clientId': client_id, 'clientOrigin': 'deviceid'}
        )
        response.raise_for_status()
        data = response.json()
        return data['clientToken']

async def emulate_progress(client_token):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://api.gamepromo.io/promo/register-event',
            headers={'Authorization': f'Bearer {client_token}'},
            json={'promoId': PROMO_ID, 'eventId': str(uuid.uuid4()), 'eventOrigin': 'undefined'}
        )
        response.raise_for_status()
        data = response.json()
        return data['hasCode']

async def generate_key(client_token):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://api.gamepromo.io/promo/create-code',
            headers={'Authorization': f'Bearer {client_token}'},
            json={'promoId': PROMO_ID}
        )
        response.raise_for_status()
        data = response.json()
        return data['promoCode']

async def generate_key_process():
    client_id = await generate_client_id()
    try:
        client_token = await login(client_id)
    except httpx.HTTPStatusError as e:
        print(f"Failed to login: {e.response.json().get('message', 'Unknown error')}")
        return None

    for _ in range(7):
        await asyncio.sleep(EVENTS_DELAY * (random.random() / 3 + 1))
        try:
            has_code = await emulate_progress(client_token)
        except httpx.HTTPStatusError as e:
            print(f"Failed to register event: {e.response.json().get('message', 'Unknown error')}")
            return None
        
        if has_code:
            break
    
    try:
        key = await generate_key(client_token)
        return key
    except httpx.HTTPStatusError as e:
        print(f"Failed to generate key: {e.response.json().get('message', 'Unknown error')}")
        return None

async def main(key_count):
    tasks = [generate_key_process() for _ in range(key_count)]
    keys = await asyncio.gather(*tasks)
    return [key for key in keys if key]

if __name__ == "__main__":
    key_count = int(input("Enter the number of keys to generate: "))
    keys = asyncio.run(main(key_count))
    if keys:
        print("Generated Keys:")
        for key in keys:
            print(key)
    else:
        print("No keys were generated.")
