from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/landing")


@router.get("/", response_class=HTMLResponse)
async def profile(request: Request):
    """
    Renders the index.html template.

    Args:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The rendered index.html template.
    """
    return templates.TemplateResponse("index.html", {"request": request})
