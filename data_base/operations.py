from sqlalchemy import insert, select, delete
from .models import UserSettings
from .config_db import async_session


async def sql_add_data(data):
    try:
        async with async_session() as session:
            stat = insert(UserSettings).values(**data)
            await session.execute(stat)
            await session.commit()
            return True
    except Exception as error:
        print(f"Error occurred while adding data: {error}")
        return False

