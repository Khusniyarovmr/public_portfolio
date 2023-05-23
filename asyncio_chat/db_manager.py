from datetime import datetime

import aiosqlite

from logger import logger


async def create_table():
    create_query = (
        "CREATE TABLE message ("
            "id INTEGER PRIMARY KEY,"
            "time REAL,"
            "from_name TEXT,"
            "to_name TEXT,"
            "message TEXT,"
            "is_deleted INTEGER"
        ")"
    )
    try:
        async with aiosqlite.connect('chat_db.db') as conn:
            await conn.execute(create_query.strip())
            await conn.commit()
    except Exception as e:
        logger.warning(f'DB_error_1: {e}')


async def insert_message_into_db(from_name: str, to_name: str, message: str) -> None:
    current_time = datetime.now().timestamp()
    query = (
        "INSERT INTO message ('time', 'from_name', 'to_name', 'message', 'is_deleted')"
        f"VALUES ({current_time}, '{from_name}', '{to_name}', '{message}', 0)"
    )

    try:
        async with aiosqlite.connect('chat_db.db') as conn:
            await conn.execute(query.strip())
            await conn.commit()
    except Exception as e:
        logger.warning(f'DB_error_2: {e}')


async def _delete_message_by_timeout(timeout: int) -> None:
    current_time = datetime.now().timestamp()
    query = (
        f"UPDATE message SET is_deleted = 1 WHERE {current_time} - time > {timeout} "
        "AND is_deleted = 0"
    )
    try:
        async with aiosqlite.connect('chat_db.db') as conn:
            await conn.execute(query)
            await conn.commit()
    except Exception as e:
        logger.warning(f'DB_error_3: {e}')


async def get_old_messages_when_online(name: str, limit: int, timeout: int) -> list | None:
    await _delete_message_by_timeout(timeout)
    query = (
        "SELECT from_name, to_name, message"
        " FROM message"
        f" WHERE (from_name = '{name}' or (to_name = '{name}' or to_name = 'ALL')) and is_deleted = 0"
        " ORDER BY time asc"
        f" LIMIT {limit}"
    )

    try:
        async with aiosqlite.connect('chat_db.db') as conn:
            async with conn.execute(query.strip()) as cursor:
                messages = await cursor.fetchall()
    except Exception as e:
        logger.warning(f'DB_error_4: {e}')
    else:
        return messages
