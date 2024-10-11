from typing import Annotated

from fastapi import Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from patrocars.dependencies import get_manufacturer_repository, templates
from patrocars.models import Manufacturer
from patrocars.persistence.repositories import ManufacturerRepository
from patrocars.schemas import ManufacturerInput

manufacturer_router = APIRouter(prefix="/montadoras")


@manufacturer_router.get("/criar")
def create_manufacturer(request: Request):
    return templates.TemplateResponse(request, "montadoras_form.html")


@manufacturer_router.post("/criar/processar_form")
def process_manufacturer_form(
    request: Request,
    manufacturer_in: Annotated[ManufacturerInput, Form()],
    manufactory_repository: ManufacturerRepository = Depends(get_manufacturer_repository),
):
    new_manufacturer = Manufacturer(**manufacturer_in.model_dump())
    manufactory_repository.create_manufacturer(new_manufacturer)
    return RedirectResponse(manufacturer_router.url_path_for("create_manufacturer"), status_code=303)
