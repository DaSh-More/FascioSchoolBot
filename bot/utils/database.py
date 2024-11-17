import aiosqlite
import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        if not self.db_path.is_file():
            self.__create_database(self.db_path)

    @staticmethod
    def __create_database(path):
        create_db_path = "./assets/SQL/create_db.sql"
        default_entries_path = "./assets/SQL/default_entries.sql"

        with open(create_db_path) as f:
            create_db_code = f.read()

        with open(default_entries_path) as f:
            default_entries_code = f.read()

        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.executescript(create_db_code)
            cursor.executescript(default_entries_code)
            conn.commit()
            cursor.close()

    async def add_user(self, user_id: int, username: str = None):
        async with aiosqlite.connect(self.db_path) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
                users = await cursor.fetchall()
                if not users:
                    await cursor.execute(
                        "INSERT INTO Users (id, username, role, state) VALUES (?, ?, ?, ?)",
                        (user_id, username, "user", "runned"),
                    )
                    await conn.commit()
                    return "user added"
                return "user exist"

    async def set_user_state(self, user_id: int, state: str):
        """
        states = ["runned", "stopped"]
        """
        states = ["runned", "stopped"]
        assert state in states, f"Incorrect state {state}"
        async with aiosqlite.connect(self.db_path) as conn:
            async with conn.cursor() as cursor:
                # Проверка существования пользователя
                await cursor.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
                assert await cursor.fetchall(), "User dont exist"
                # Установка состояния
                await cursor.execute(
                    "UPDATE Users SET state = ? WHERE id = ?", (state, user_id)
                )
                await conn.commit()

    async def set_user_role(self, user_id: int, role: str):
        """
        roles = ["user", "admin"]
        """
        roles = ["user", "admin"]
        assert role in roles, f"Incorrect role {role}"
        async with aiosqlite.connect(self.db_path) as conn:
            async with conn.cursor() as cursor:
                # Проверка существования пользователя
                await cursor.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
                assert await cursor.fetchall(), "User dont exist"
                # Установка состояния
                await cursor.execute(
                    "UPDATE Users SET role = ? WHERE id = ?", (role, user_id)
                )
                await conn.commit()

    async def get_all_users(self):
        async with aiosqlite.connect(self.db_path) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT * FROM Users")
                return await cursor.fetchall()

    async def get_user(self, user_id: int | None = None, username: str | None = None):
        assert user_id or username, "Empty values"
        async with aiosqlite.connect(self.db_path) as conn:
            async with conn.cursor() as cursor:
                if user_id:
                    await cursor.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
                else:
                    await cursor.execute(
                        "SELECT * FROM Users WHERE username = ?", (username,)
                    )
                return (await cursor.fetchall())[0]
