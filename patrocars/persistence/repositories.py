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

    def get_by_id(self, cm_id: str):
        stmt = select(CarModel).where(CarModel.id == cm_id)
        return self.session.scalar(stmt)

    def create_car_model(self, new_car_model: CarModel):
        self.session.add(new_car_model)
        self.session.commit()
        self.session.refresh(new_car_model)

    def edit_car_model(self, old_car_model: CarModel, new_car_model: CarModel):
        old_car_model.description = new_car_model.description
        old_car_model.name = new_car_model.name
        old_car_model.is_automatic = new_car_model.is_automatic
        old_car_model.reference_value = new_car_model.reference_value
        self.session.commit()
        self.session.refresh(old_car_model)
        return old_car_model

    def delete_car_model(self, car_model_id: str):
        to_be_deleted = self.get_by_id(car_model_id)
        self.session.delete(to_be_deleted)
        self.session.commit()
