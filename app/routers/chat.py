from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.dependencies import is_authorized

router = APIRouter(prefix="/chatbot")
router.dependencies = [Depends(is_authorized)]
templates = Jinja2Templates(directory="app/templates")


@router.get("/qa", response_class=HTMLResponse)
async def chat_home(request: Request):
    """
    A function that handles the root route.

    Returns:
        TemplateResponse: The response containing the rendered index.html template.
    """
    return templates.TemplateResponse("chatbot.html", {"request": request})
