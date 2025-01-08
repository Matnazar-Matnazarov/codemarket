import asyncio
import time
from aiohttp import ClientSession
import requests


# Sinxron (oddiy) funksiya
def sync_fetch_data(url):
    response = requests.get(url)
    return response.text


# Asinxron funksiya
async def async_fetch_data(session, url):
    async with session.get(url) as response:
        return await response.text()


# Sinxron tarzda bir nechta so'rovlarni yuborish
def run_sync_tasks():
    urls = [
        "https://api.github.com/users/1",
        "https://api.github.com/users/2",
        "https://api.github.com/users/3",
        "https://api.github.com/users/4",
        "https://api.github.com/users/5",
    ] * 100

    start_time = time.time()

    # Har bir URL uchun ketma-ket so'rov yuborish
    for url in urls:
        sync_fetch_data(url)

    end_time = time.time()
    return end_time - start_time


# Asinxron tarzda bir nechta so'rovlarni yuborish
async def run_async_tasks():
    urls = [
        "https://api.github.com/users/1",
        "https://api.github.com/users/2",
        "https://api.github.com/users/3",
        "https://api.github.com/users/4",
        "https://api.github.com/users/5",
    ] * 100

    start_time = time.time()

    async with ClientSession() as session:
        # Barcha so'rovlarni bir vaqtda yuborish
        tasks = [async_fetch_data(session, url) for url in urls]
        await asyncio.gather(*tasks)

    end_time = time.time()
    return end_time - start_time


# Asosiy funksiya
async def main():
    # Sinxron usulni tekshirish
    sync_time = run_sync_tasks()
    print(f"Sinxron usul vaqti: {sync_time:.2f} sekund")

    # Asinxron usulni tekshirish
    async_time = await run_async_tasks()
    print(f"Asinxron usul vaqti: {async_time:.2f} sekund")

    # Tezlik farqini hisoblash
    speedup = sync_time / async_time
    print(f"Asinxron usul {speedup:.2f} marta tezroq ishladi")


# Dasturni ishga tushirish
if __name__ == "__main__":
    asyncio.run(main())
