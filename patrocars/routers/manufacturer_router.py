from typing import Annotated
from uuid import UUID

from fastapi import Depends, Form, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from patrocars.dependencies import get_car_model_repository, get_manufacturer_repository, templates
from patrocars.models import Manufacturer
from patrocars.persistence.repositories import CarModelRepository, ManufacturerRepository
from patrocars.schemas import ManufacturerInput

manufacturer_router = APIRouter(prefix="/montadoras")


@manufacturer_router.get("/criar")
def create_manufacturer(request: Request):
    return templates.TemplateResponse(request, "montadoras/form.html")


@manufacturer_router.post("/criar/processar_form")
def process_manufacturer_form(
    request: Request,
    manufacturer_in: Annotated[ManufacturerInput, Form()],
    manufactory_repository: ManufacturerRepository = Depends(get_manufacturer_repository),
):
    new_manufacturer = Manufacturer(**manufacturer_in.model_dump())
    manufactory_repository.create_manufacturer(new_manufacturer)
    return RedirectResponse(manufacturer_router.url_path_for("create_manufacturer"), status_code=303)


@manufacturer_router.get("/{m_id}")
def manufacturer_detail(
    m_id: UUID,
    request: Request,
    manufactory_repository: ManufacturerRepository = Depends(get_manufacturer_repository),
):
    manufacturer = manufactory_repository.get_by_id(m_id)
    if not manufacturer:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Manufacturer with this id not found")
    return templates.TemplateResponse(request, "montadoras/detail.html", context={"montadora": manufacturer})
