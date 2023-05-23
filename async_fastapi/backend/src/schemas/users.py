from pydantic import BaseModel

class UserModel(BaseModel):
    username: str
    first_name: str
    last_name: str
    role_id: int
    email: str
    telegram_chat_id: int
    is_superuser: bool

class UserCreate(UserModel):
    pass


class UserUpdate(UserModel):
    pass

