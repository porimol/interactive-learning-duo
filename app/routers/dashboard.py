from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.dependencies import is_authorized
from app.db.dashboardstats import get_question_stats, get_question_ratio
from app.config import MONTH_NAMES

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
    user_id = request.session["USER_ID"]
    question_stats = question_stats_to_dict(user_id)
    question_ratio = question_stats_ratio(user_id)

    return templates.TemplateResponse(
        "dashboard.html", {
            "request": request,
            "question_stats": question_stats,
            "question_ratio": question_ratio
        })


def question_stats_to_dict(user_id):
    """
    Converts the question statistics from a list of tuples to a dictionary.

    Args:
        question_stats (list): A list of tuples containing the question statistics.

    Returns:
        dict: A dictionary containing the question statistics.
    """
    question_stats = get_question_stats(user_id)
    months = []
    frequency = []
    for question_stat in question_stats:
        months.append(MONTH_NAMES[question_stat[0]])
        frequency.append(question_stat[2])
    stats = {
        "months": months,
        "frequency": frequency
    }
    return stats


def question_stats_ratio(user_id):
    """
    Converts the question statistics from a list of tuples to a dictionary.

    Args:
        question_stats (list): A list of tuples containing the question statistics.

    Returns:
        dict: A dictionary containing the question statistics.
    """
    question_stats = get_question_ratio(user_id)
    if not question_stats:
        return {"python": 0, "sql": 0}
    question_stats = {key: value for key, value in question_stats}
    
    return question_stats
