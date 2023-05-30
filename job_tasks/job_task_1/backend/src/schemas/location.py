from pydantic import BaseModel


class LocationBaseModel(BaseModel):
    city: str
    state: str
    zip_code: str
    latitude: float
    longitude: float


class LocationModel(LocationBaseModel):
    id: int

    class Config:
        orm_mode = True


class LocationCreate(LocationBaseModel):
    pass

    class Config:
        orm_mode = True


class LocationUpdate(LocationModel):
    pass
