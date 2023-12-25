from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.dependencies import is_authorized
from jose import jwt

router = APIRouter(prefix="/dashboard")
router.dependencies = [Depends(is_authorized)]
templates = Jinja2Templates(directory="app/templates")


@router.get("/home", response_class=HTMLResponse)
async def chat_home(request: Request):
    """
    A function that handles the dashboard route.

    Returns:
        TemplateResponse: The response containing the rendered dashboard.html template.
    """
    return templates.TemplateResponse("dashboard.html", {"request": request})