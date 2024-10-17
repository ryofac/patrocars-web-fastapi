from typing import Annotated
from uuid import UUID

from fastapi import Depends, Form, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from patrocars.dependencies import get_manufacturer_repository, templates
from patrocars.models import Manufacturer
from patrocars.persistence.repositories import ManufacturerRepository
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
    return RedirectResponse(
        url="/home",
        status_code=303,
    )


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


@manufacturer_router.get("/editar/{m_id}/")
def manufacturer_update(
    m_id: str,
    request: Request,
    manufacturer_repository: ManufacturerRepository = Depends(get_manufacturer_repository),
):
    manufacturer = manufacturer_repository.get_by_id(m_id)
    if not manufacturer:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Manufacturer with this id not found")
    return templates.TemplateResponse(request, "montadoras/form_update.html", context={"montadora": manufacturer})


@manufacturer_router.post("/editar/{m_id}/processar_form")
def manufacturer_process_update(
    m_id: str,
    request: Request,
    new_manufacturer: Annotated[ManufacturerInput, Form()],
    manufacturer_repository: ManufacturerRepository = Depends(get_manufacturer_repository),
):
    old_manufacturer = manufacturer_repository.get_by_id(m_id)
    if not old_manufacturer:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Manufacturer with this id not found")

    manufacturer_repository.edit_manufacturer(old_manufacturer, new_manufacturer)

    return RedirectResponse(
        url="/home",
        status_code=303,
    )


@manufacturer_router.get("/deletar/{m_id}")
def manufacturer_delete(
    m_id: str,
    request: Request,
    manufacturer_repository: ManufacturerRepository = Depends(get_manufacturer_repository),
):
    manufacturer = manufacturer_repository.get_by_id(m_id)
    if not manufacturer:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Manufacturer with this id not found")

    car_model_amount = len(manufacturer.car_models)

    return templates.TemplateResponse(
        request,
        "montadoras/form_delete.html",
        context={"montadora": manufacturer, "quantidade_carros": car_model_amount},
    )


@manufacturer_router.post("/deletar/{m_id}/processar_form")
def manufacturer_process_delete(
    m_id: str,
    request: Request,
    manufacturer_repository: ManufacturerRepository = Depends(get_manufacturer_repository),
):
    old_manufacturer = manufacturer_repository.get_by_id(m_id)
    if not old_manufacturer:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Manufacturer with this id not found")

    manufacturer_repository.delete_manufacturer(m_id)

    return RedirectResponse(
        url="/home",
        status_code=303,
    )
