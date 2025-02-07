from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select, delete, text, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import Base, db_session


class NotFoundError(Exception):
    pass


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class Repository:

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    @db_session
    async def get(self, db: AsyncSession, obj_id: Any) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.id == obj_id)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    @db_session
    async def get_multi(
            self, db: AsyncSession, *, skip=0, limit=100
    ) -> List[ModelType]:
        statement = select(self._model).offset(skip).limit(limit)
        results = await db.execute(statement=statement)
        return results.scalars().all()

    @db_session
    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self._model(**dict(obj_in))
        db.add(db_obj)
        try:
            await db.commit()
            await db.refresh(db_obj)
        except Exception as e:
            await db.rollback()
            raise e
        return db_obj

    @db_session
    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType,
            obj_in: UpdateSchemaType | Dict[str, Any]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            obj_data = obj_in
        else:
            obj_data = dict(obj_in)
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @db_session
    async def delete(self, db: AsyncSession, *, obj_id: int | str):
        record = await db.get(self._model, obj_id)
        if record is None:
            raise NotFoundError(f"No record with id {obj_id} found!")
        delete_stmt = delete(self._model).where(self._model.id == obj_id)
        await db.execute(delete_stmt)
        await db.commit()

    @staticmethod
    def get_order_expression(sort_field: str, sort_dir: str):
        if sort_dir.lower() == 'desc':
            order_expr = desc(text(sort_field))
        else:
            order_expr = text(sort_field)
        return order_expr
