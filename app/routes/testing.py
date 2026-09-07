from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[2]
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@router.get("/testing", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="testing.html")


# Examples
# @router.get("/testing")
# def testing_page():
#     ...

# @router.post("/testing")
# def run_test():
#     ...