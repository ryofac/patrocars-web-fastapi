from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from patrocars.database import get_db
from patrocars.models import Manufacturer

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    redirect_slashes=True,
)

templates = Jinja2Templates("patrocars/templates/")


@app.get("/")
def redirect_to_home():
    return RedirectResponse("/home", status_code=status.HTTP_301_MOVED_PERMANENTLY)


@app.get("/home")
def home(request: Request, db: Session = Depends(get_db)):
    _context = {}
    manufacturers = db.scalars(select(Manufacturer)).all()
    _context["manufacturers"] = manufacturers
    return templates.TemplateResponse(request, "home.html", context=_context)


@app.get("/montadoras/criar")
def create_montadora(request: Request):
    return templates.TemplateResponse(request, "montadoras_form.html")
