from src.crud.base import RepositoryDB
from src.models import Message, Log
from src.schemes.message import MessageCreate, MessageUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import db_session
from sqlalchemy import select, text


class CRUDMessage(RepositoryDB[Message, MessageCreate, MessageUpdate]):

    @db_session
    async def get_report_by_address(self, db: AsyncSession, address: str):
        statement = text(
            f"""
            with t1 as (
                select l.int_id, l.created, l.str_row 
                from public.log l 
                where l.address = '{address}'
            ),
            t2 as (
                select m.int_id, m.created, m.str_row 
                from public.message m
                where m.int_id in (select distinct int_id from t1)
            ),
            t3 as (
                select int_id, created, str_row from t1
                union
                select int_id, created, str_row from t2
            )
            
            select created, str_row from t3 order by int_id, created
            """
        )
        results = await db.execute(statement=statement)
        return results.fetchall()


message_crud = CRUDMessage(Message)
