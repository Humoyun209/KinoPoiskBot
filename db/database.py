import aiosqlite


class DataBase:
    def __init__(self, name) -> None:
        self.name = name
    
    async def create_user(self, user_id, username):
        async with aiosqlite.connect(self.name) as db:
            if not await self.get_me(user_id):
                await db.execute('INSERT INTO users(user_id, username) VALUES (?, ?)', (user_id, username))
                await db.commit()
            else:
                pass
    
    async def get_me(self, user_id):
        async with aiosqlite.connect(self.name) as db:
            result = await db.execute('SELECT * FROM users WHERE user_id = ?', (user_id, ))
            return await result.fetchone()

