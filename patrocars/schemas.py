from pydantic import BaseModel


class ManufacturerInput(BaseModel):
    name: str
    country: str
    foundation_year: int


class CarModelInput(BaseModel):
    pass
