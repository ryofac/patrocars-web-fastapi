from sqlalchemy import select
from sqlalchemy.orm import Session

from patrocars.models import Manufacturer


class ManufacturerRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        stmt = select(Manufacturer)
        return self.session.scalars(stmt).all()

    def create_manufacturer(self, new_manufacturer: Manufacturer):
        self.session.add(new_manufacturer)
        self.session.commit()
        self.session.refresh(new_manufacturer)
        return new_manufacturer
