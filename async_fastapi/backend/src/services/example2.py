from src.db.db import async_session, get_session, engine
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio


async def main(db: AsyncSession = engine):
    print()
    session = db
    print()





if __name__=='__main__':
    asyncio.run(main())