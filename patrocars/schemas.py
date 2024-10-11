from pydantic import BaseModel


class ManufacturerInput(BaseModel):
    name: str
    country: str
    foundation_year: int


class CarModelInput(BaseModel):
    name: str
    reference_value: float
    motorization: float
    description: str
    is_automatic: str | None
