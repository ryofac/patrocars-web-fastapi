from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import SQLAlchemyError

from patrocars.dependencies import get_manufacturer_repository, templates
from patrocars.persistence.repositories import ManufacturerRepository
from patrocars.routers.manufacturer_router import manufacturer_router

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    redirect_slashes=True,
)


app.include_router(manufacturer_router)


@app.exception_handler(SQLAlchemyError)
def handle_db_error(request: Request, exc: SQLAlchemyError):
    return templates.TemplateResponse(
        request,
        "errors/500.html",
        {"error_message": str(exc)},
    )


@app.get("/500")
def quinhentos(request: Request):
    return templates.TemplateResponse(
        request,
        "errors/500.html",
        {"error_message": "An unknown error ocurred"},
    )


@app.get("/")
def redirect_to_home():
    return RedirectResponse("/home", status_code=status.HTTP_301_MOVED_PERMANENTLY)


@app.get("/home")
def home(request: Request, manufacturer_repository: ManufacturerRepository = Depends(get_manufacturer_repository)):
    _context = {}
    manufacturers = manufacturer_repository.get_all()
    _context["manufacturers"] = manufacturers
    return templates.TemplateResponse(request, "home.html", context=_context)
