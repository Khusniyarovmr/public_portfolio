from pydantic import BaseModel


class UserAccountInfoModel(BaseModel):
    user_id: int
    type: str
    balance: float

class UserAccountInfoCreate(UserAccountInfoModel):
    pass


class UserAccountInfoUpdate(UserAccountInfoModel):
    pass

