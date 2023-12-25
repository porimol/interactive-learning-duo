from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.db.sql import create_user, get_user_by_email
from app.config import AUTH_SESSION_NAME
from app.dependencies import is_authorized, get_access_token, PWD_CONTEXT


router = APIRouter(prefix="/auth")
templates = Jinja2Templates(directory="app/templates")


def authenticate_user(email, password):
    """
    Authenticates a user by checking if the provided email and password match the stored credentials.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        dict or bool: If the authentication is successful, returns the user dictionary. Otherwise, returns False.
    """
    user = get_user_by_email(email)
    if not user:
        return False
    if not PWD_CONTEXT.verify(password, user["password"]):
        return False
    user.pop('photo')
    return user


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    """
    Handle the login request.

    Args:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The response containing the login.html template.
    """
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(request: Request):
    """
    Handle the login request.

    Args:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The response containing the login.html template.
    """
    try:
        form = await request.form()
        user_email = form.get("email", None)
        user_password = form.get("password", None)
        
        if not user_email or not user_password:
            return templates.TemplateResponse("login.html", {
                "request": request,
                "error": "Invalid username or password"
            })
        
        user = authenticate_user(user_email, user_password)
        if user is False:
            return templates.TemplateResponse("login.html", {
                "request": request,
                "error": "Invalid username or password"
            })
        request.session[AUTH_SESSION_NAME] = get_access_token({"sub": user})
        request.session["USER_ID"] = user.get('id')
        request.session["FULL_NAME"] = f"{user.get('first_name')} {user.get('last_name')}"
        return RedirectResponse("/dashboard/home", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        print(e)
        return RedirectResponse("/auth/login?error=Something went wrong. Please try again later.", status_code=status.HTTP_302_FOUND)


@router.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    """
    Register a new user.

    Args:
        request (Request): The incoming request.

    Returns:
        TemplateResponse: The template response for the register page.
    """
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register(request: Request):
    """
    Register a new user.

    Args:
        request (Request): The incoming request.

    Returns:
        TemplateResponse: The template response for the register page.
    """
    form = await request.form()
    first_name = form.get("first_name")
    last_name = form.get("last_name")
    email = form.get("email")
    password = form.get("password")
    password_repeat = form.get("password_repeat")

    if password != password_repeat:
        return templates.TemplateResponse("register.html", {
            "request": request, 
            "error": "Passwords do not match"
        })
    
    hashed_password = PWD_CONTEXT.hash(password)
    is_user_created = create_user(first_name, last_name, email, hashed_password)
    if is_user_created:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "success": "Registration successful"
        })
    return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Registration failed"
        })


@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password(request: Request):
    """
    Handle the forgot password request.

    Args:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The template response for the forgot password page.
    """
    return templates.TemplateResponse("forgot-password.html", {"request": request})


@router.get("/logout", dependencies=[Depends(is_authorized)])
async def logout(request: Request):
    """
    Logs out the user and returns a message indicating successful logout.
    """
    request.session.pop(AUTH_SESSION_NAME, None)

    if request.session.get(AUTH_SESSION_NAME) is None:
        return RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)
