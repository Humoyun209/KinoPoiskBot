import datetime
from sqlite3 import ProgrammingError

import aiosqlite
from datetime import datetime, date,


class DataBase:
    def __init__(self, name) -> None:
        self.name = name

    @staticmethod
    def get_date(to_time: str | None = None) -> str | datetime:
        format_date = '%Y-%m-%d %H:%M:%S'
        if to_time is not None:
            return datetime.strptime(to_time, format_date)
        now = datetime.now()
        now_str = now.strftime(format_date)
        return now_str
    
    async def create_user(self, user_id, username):
        async with aiosqlite.connect(self.name) as db:
            if not await self.get_me(user_id):
                await db.execute('INSERT INTO users(user_id, username, joined, last_time) VALUES (?, ?)', (user_id, username))
                await db.commit()
            else:
                pass
    
    async def get_me(self, user_id):
        async with aiosqlite.connect(self.name) as db:
            result = await db.execute('SELECT * FROM users WHERE user_id = ?', (user_id, ))
            return await result.fetchone()

    async def save_query(self, user_id, query):
        async with aiosqlite.connect(self.name) as db:
            now = self.get_date()
            try:
                await db.execute('INSERT INTO history_queries(query, created, user_id) VALUES(?, ?, ?)', (query, user_id, now))
            except ProgrammingError as e:
                pass


