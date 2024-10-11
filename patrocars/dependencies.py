from fastapi import Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from patrocars.persistence.database import get_db
from patrocars.persistence.repositories import CarModelRepository, ManufacturerRepository

static = StaticFiles(directory="patrocars/static/")
templates = Jinja2Templates("patrocars/templates/")


def get_manufacturer_repository(session: Session = Depends(get_db)):
    return ManufacturerRepository(session)


def get_car_model_repository(session: Session = Depends(get_db)):
    return CarModelRepository(session)
