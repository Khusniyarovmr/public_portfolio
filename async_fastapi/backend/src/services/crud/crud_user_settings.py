from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import secure_api_secret, secure_api_key
from src.models.user_settings import UserSettings
from src.schemas.user_settings import UserSettingsCreate, UserSettingsUpdate
from .base import RepositoryDB


class CRUDUserSettings(RepositoryDB[UserSettings, UserSettingsCreate, UserSettingsUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: UserSettingsCreate) -> UserSettings:
        new_obj_in_data = {
            "user_id": obj_in.user_id,
            "stock_market": obj_in.stock_market,
            "hashed_key": secure_api_key(obj_in.hashed_key, 365),
            "hashed_secret": secure_api_secret(obj_in.hashed_secret, 365)
        }
        db_obj = self._model(**new_obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


user_settings_crud = CRUDUserSettings(UserSettings)
