import aiosqlite
from config import DB_PATH


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS message_map (
                admin_chat_id INTEGER,
                admin_message_id INTEGER,
                user_id INTEGER,
                PRIMARY KEY (admin_chat_id, admin_message_id)
            )
        """)
        await db.commit()


async def save_mapping(admin_chat_id: int, admin_message_id: int, user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO message_map (admin_chat_id, admin_message_id, user_id) VALUES (?, ?, ?)",
            (admin_chat_id, admin_message_id, user_id),
        )
        await db.commit()


async def get_user_for_reply(admin_chat_id: int, admin_message_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT user_id FROM message_map WHERE admin_chat_id=? AND admin_message_id=?",
            (admin_chat_id, admin_message_id),
        )
        row = await cur.fetchone()
        return row[0] if row else None
