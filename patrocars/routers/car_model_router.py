from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from patrocars.dependencies import get_car_model_repository, get_manufacturer_repository, templates
from patrocars.models import CarModel
from patrocars.persistence.repositories import CarModelRepository, ManufacturerRepository
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
    print(new_car_model)

    owner_man = manufacturer_repository.get_by_id(manufacturer_id)
    if not owner_man:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Manufacturer assossiated not found")

    new_car_is_automatic = bool(new_car_model.is_automatic) if new_car_model else False
    car_model: CarModel = CarModel(
        **new_car_model.model_dump(exclude="is_automatic"),
        manufacturer_id=owner_man.id,
        is_automatic=new_car_is_automatic,
    )
    car_model_repository.create_car_model(car_model)
    return RedirectResponse(
        car_model_router.url_path_for("car_model_form", manufacturer_id=manufacturer_id),
        status_code=status.HTTP_303_SEE_OTHER,
    )
