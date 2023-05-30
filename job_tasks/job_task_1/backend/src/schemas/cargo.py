from datetime import datetime

from pydantic import BaseModel


class CargoBaseModel(BaseModel):
    pick_up_location: str
    delivery_location: str
    weight: int
    description: str


class CargoModel(CargoBaseModel):
    id: int
    create_Date: datetime

    class Config:
        orm_mode = True


class CargoCreate(CargoBaseModel):
    pass

    class Config:
        orm_mode = True


class CargoUpdate(BaseModel):
    weight: int | None
    description: str | None
    id: int

    class Config:
        orm_mode = True


class ListOfTrucks(BaseModel):
    truck_id: int
    distance: float


class CargoModelWithAllTrucks(CargoBaseModel):
    trucks: list[ListOfTrucks]


class CargoWithTruckCountBase(BaseModel):
    pick_up_location: str
    delivery_location: str
    trucks: int
