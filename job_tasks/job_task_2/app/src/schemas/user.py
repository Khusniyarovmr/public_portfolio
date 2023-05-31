from pydantic import BaseModel


class UserModel(BaseModel):
    phone_number: str
    address: str

