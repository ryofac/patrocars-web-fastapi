from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from patrocars.dependencies import get_car_model_repository, get_manufacturer_repository, templates
from patrocars.models import CarModel
from patrocars.persistence.repositories import CarModelRepository, ManufacturerRepository
from patrocars.routers.manufacturer_router import manufacturer_router
from patrocars.schemas import CarModelInput

car_model_router = APIRouter(prefix="/modelo_carro")


@car_model_router.get("/criar/{manufacturer_id}")
def car_model_form(
    manufacturer_id: str,
    request: Request,
    manufacturer_repository: ManufacturerRepository = Depends(get_manufacturer_repository),
):
    man_owner = manufacturer_repository.get_by_id(manufacturer_id)
    if not man_owner:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Car manufacturer not found!")
    return templates.TemplateResponse(request, "modelo_carros/form.html", {"montadora": man_owner})


@car_model_router.post("/criar/{manufacturer_id}/processar_form")
def car_model_process_form(
    request: Request,
    manufacturer_id: str,
    new_car_model: Annotated[CarModelInput, Form()],
    car_model_repository: CarModelRepository = Depends(get_car_model_repository),
    manufacturer_repository: ManufacturerRepository = Depends(get_manufacturer_repository),
):
    owner_man = manufacturer_repository.get_by_id(manufacturer_id)
    if not owner_man:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Manufacturer assossiated not found")

    new_car_is_automatic = True if new_car_model.is_automatic.lower() == "true" else False
    car_model: CarModel = CarModel(
        **new_car_model.model_dump(exclude="is_automatic"),
        manufacturer_id=owner_man.id,
        is_automatic=new_car_is_automatic,
    )
    car_model_repository.create_car_model(car_model)
    return RedirectResponse(
        manufacturer_router.url_path_for("manufacturer_detail", m_id=manufacturer_id),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@car_model_router.get("/deletar/{car_model_id}")
def car_model_delete(
    request: Request,
    car_model_id: str,
    car_model_repository: CarModelRepository = Depends(get_car_model_repository),
):
    car_model = car_model_repository.get_by_id(car_model_id)
    return templates.TemplateResponse(request, "modelo_carros/form_delete.html", {"modelo_carro": car_model})


@car_model_router.post("/deletar/{car_model_id}/processar_form")
def car_model_process_delete(
    request: Request,
    car_model_id: str,
    car_model_repository: CarModelRepository = Depends(get_car_model_repository),
):
    existent_car_model = car_model_repository.get_by_id(car_model_id)
    if not existent_car_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car model not found!")
    manufacturer_id = existent_car_model.manufacturer.id
    car_model_repository.delete_car_model(car_model_id)
    return RedirectResponse(
        manufacturer_router.url_path_for("manufacturer_detail", m_id=manufacturer_id),
        status_code=301,
    )
