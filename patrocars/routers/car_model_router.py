from fastapi import APIRouter, Depends, HTTPException, Request, status

from patrocars.dependencies import get_car_model_repository, get_manufacturer_repository, templates
from patrocars.persistence.repositories import CarModelRepository, ManufacturerRepository

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
def car_model_process_form(request: Request):
    pass
