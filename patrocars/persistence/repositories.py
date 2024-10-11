from sqlalchemy import select
from sqlalchemy.orm import Session

from patrocars.models import CarModel, Manufacturer


class ManufacturerRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, m_id: str):
        stmt = select(Manufacturer).where(Manufacturer.id == m_id)
        return self.session.scalar(stmt)

    def get_all(self):
        stmt = select(Manufacturer)
        return self.session.scalars(stmt).all()

    def create_manufacturer(self, new_manufacturer: Manufacturer):
        self.session.add(new_manufacturer)
        self.session.commit()
        self.session.refresh(new_manufacturer)
        return new_manufacturer


class CarModelRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self):
        stmt = select(CarModel)
        return self.session.scalars(stmt).all()

    def create_car_model(self, new_car_model: CarModel):
        self.session.add(new_car_model)
        self.session.commit()
        self.session.refresh(new_car_model)
