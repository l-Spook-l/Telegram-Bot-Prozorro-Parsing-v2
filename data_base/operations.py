from sqlalchemy import insert, select, delete
from .models import UserSettings
from .config_db import async_session


async def orm_add_data(data) -> bool:
    try:
        async with async_session() as session:
            stat = insert(UserSettings).values(**data)
            await session.execute(stat)
            await session.commit()
            return True
    except Exception as error:
        print(f"Error occurred while adding data: {error}")
        return False


async def orm_get_data(message):
    try:
        async with async_session() as session:
            query = select(UserSettings).filter_by(user=message.from_user.id)
            result = await session.execute(query)
        return result.scalars().all()
    except Exception as error:
        print(f"Error occurred while reading data: {error}")
        return False


async def orm_read_time(time_now):
    try:
        async with async_session() as session:
            query = select(UserSettings).filter_by(Dispatch_time=time_now)
            res = await session.execute(query)
            result = res.all()
        return result
    except Exception as error:
        print(f"Error occurred while check time: {error}")


async def orm_delete_data(id):
    try:
        async with async_session() as session:
            query = delete(UserSettings).filter_by(id=id)
            await session.execute(query)
            await session.commit()
        return True
    except Exception as error:
        print(f"Error occurred while remove data: {error}")
        return False
