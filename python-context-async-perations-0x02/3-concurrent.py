import aiosqlite
import asyncio

async def async_fetch_users():
    async with aiosqlite.connect("mydb.sqlite") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All Users:", users)

async def async_fetch_older_users():
    async with aiosqlite.connect("mydb.sqlite") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("Users older than 40:", older_users)

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

asyncio.run(fetch_concurrently())
