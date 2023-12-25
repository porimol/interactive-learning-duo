from datetime import datetime
from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.dependencies import is_authorized
from app.db.qa import insert_question, get_todays_qa_by_userid

router = APIRouter(prefix="/chatbot")
router.dependencies = [Depends(is_authorized)]
templates = Jinja2Templates(directory="app/templates")


@router.get("/qa", response_class=HTMLResponse)
async def chat_home(request: Request):
    """
    This function handles the chat home page request.

    Args:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The template response containing the chatbot.html template, request object, and questions.
    """
    today_date = datetime.now().strftime("%Y-%m-%d")
    user_id = request.session["USER_ID"]
    questions = get_todays_qa_by_userid(user_id, today_date)
    return templates.TemplateResponse(
        "chatbot.html", {
            "request": request,
            "questions": questions,
            # "error": error
        })


@router.post("/qa", response_class=HTMLResponse)
async def question_answer(request: Request):
    """
    Handles POST requests to the "/qa" route. This function takes a user's question, 
    validates the form data, and inserts the question into the database.

    Args:
        request (Request): The request object containing all the HTTP information.

    Returns:
        RedirectResponse: A redirection to "/chatbot/qa" if the question was successfully inserted.
        If there were any empty fields in the form or if the insertion failed, it redirects to 
        "/chatbot/qa" with an appropriate error message.
    """

    form = await request.form()
    empty_fields = [field.replace("_", " ") for field, value in form.items() if not value]
    
    if empty_fields:
        message = f"Empty fields: {', '.join(empty_fields)}"
        return RedirectResponse(f"/chatbot/qa?error={message}", status_code=status.HTTP_302_FOUND)
    
    user_id = request.session["USER_ID"]
    question = form.get("question")
    answer = ""
    question_category = "python"
    today_date = datetime.now().strftime("%Y-%m-%d %I:%M")
    insert_rsp = insert_question(user_id, question, answer, question_category, today_date)
    if insert_rsp:
        return RedirectResponse("/chatbot/qa", status_code=status.HTTP_302_FOUND)
    
    return RedirectResponse("/chatbot/qa?error=Something went wrong", status_code=status.HTTP_302_FOUND)

