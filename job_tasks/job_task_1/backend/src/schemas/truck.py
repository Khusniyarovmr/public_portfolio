from pydantic import BaseModel


class TruckBaseModel(BaseModel):
    truck_number: str
    location_id: int
    capacity: int
    is_active: int


class TruckModel(TruckBaseModel):
    id: int

    class Config:
        orm_mode = True


class TruckCreate(TruckBaseModel):
    pass

    class Config:
        orm_mode = True


class TruckUpdate(TruckModel):
    pass


class TruckUpdateById(BaseModel):
    id: int
    zip_code: str
