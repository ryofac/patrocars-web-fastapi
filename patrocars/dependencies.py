from pathlib import Path

from fastapi import Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from patrocars.persistence.database import get_db
from patrocars.persistence.repositories import CarModelRepository, ManufacturerRepository

# Caminho absoluto baseado no diretório raiz
BASE_DIR = Path(__file__).resolve().parent

static = StaticFiles(directory=str(BASE_DIR / "static"))
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def get_manufacturer_repository(session: Session = Depends(get_db)):
    return ManufacturerRepository(session)


def get_car_model_repository(session: Session = Depends(get_db)):
    return CarModelRepository(session)
