import io
from base64 import b64encode
import imghdr
from fastapi import (APIRouter, Request, Depends, status,
                     UploadFile, File, HTTPException)
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from app.dependencies import is_authorized, PWD_CONTEXT
from app.db.user import (get_user_by_id, update_user, update_photo,
                         get_photo_by_user_id, update_password)
from app.db.address import (count_user_address, get_user_address_by_id,
                            update_user_address)


router = APIRouter(prefix="/user")
router.dependencies = [Depends(is_authorized)]
templates = Jinja2Templates(directory="app/templates")


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    """
    Renders the profile.html template.

    Args:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The rendered profile.html template.
    """
    user_id = request.session["USER_ID"]
    user = get_user_by_id(user_id)
    success = request.query_params.get("success", None)
    error = request.query_params.get("error", None)

    user_address = get_user_address_by_id(user_id)
    user["address"] = user_address
    if not user.get("photo"):
        user["profile_photo"] = None
    if user.get("photo"):
        user["profile_photo"] = b64encode(user.get("photo", "")).decode('utf-8')

    return templates.TemplateResponse(
        "profile.html", {
            "request": request,
            "user": user,
            "success": success,
            "error": error
        })


@router.post("/profile", response_class=HTMLResponse)
async def update_profile(request: Request):
    """
    Updates the user profile.

    Args:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The rendered profile.html template.
    """
    form = await request.form()
    empty_fields = [field.replace("_", " ") for field, value in form.items() if not value]
    
    if empty_fields:
        message = f"Empty fields: {', '.join(empty_fields)}"
        return RedirectResponse(f"/user/profile?error={message}", status_code=status.HTTP_302_FOUND)
    
    first_name = form.get("first_name")
    last_name = form.get("last_name")
    email = form.get("email")
    update_rsp = update_user(
        request.session["USER_ID"],
        first_name,
        last_name,
        email
    )
    if update_rsp:
        request.session["FULL_NAME"] = f"{first_name} {last_name}"
        return RedirectResponse("/user/profile?success=Profile updated successfully", status_code=status.HTTP_302_FOUND)
    
    return RedirectResponse("/user/profile?error=Error updating profile", status_code=status.HTTP_302_FOUND)


@router.post("/address-update", response_class=HTMLResponse)
async def update_address(request: Request):
    """
    Updates the user profile.

    Args:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The rendered profile.html template.
    """
    address = await request.form()
    empty_fields = [field.replace("_", " ") for field, value in address.items() if not value]
    
    if empty_fields:
        message = f"Empty fields: {', '.join(empty_fields)}"
        return RedirectResponse(f"/user/profile?error={message}", status_code=status.HTTP_302_FOUND)
    
    user_id = request.session["USER_ID"]
    user_address = get_user_address_by_id(user_id)
    address_id = user_address.get("id", count_user_address()+1)
    update_rsp = update_user_address(address_id, user_id, address)

    if update_rsp:
        return RedirectResponse("/user/profile?success=Profile updated successfully", status_code=status.HTTP_302_FOUND)
    return RedirectResponse("/user/profile?error=Error updating profile", status_code=status.HTTP_302_FOUND)


@router.get("/profile-photo")
async def display_image(request: Request):
    """
    Display the user's image based on the user ID.

    Args:
        request (Request): The incoming request object.

    Returns:
        StreamingResponse: The streaming response containing the user's image.

    Raises:
        HTTPException: If the user's image is not found.
    """
    user_id = request.session.get("USER_ID", None)
    user = get_photo_by_user_id(user_id)

    if user:
        return StreamingResponse(io.BytesIO(user.get("photo", None)), media_type="image/jpeg")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


@router.post("/photo-upload")
async def upload_file(request: Request, file: UploadFile = File()):
    """
    Uploads a file and updates the user's photo.

    Parameters:
        request (Request): The request object.
        file (UploadFile, optional): The file to be uploaded. Defaults to File().

    Returns:
        dict: A dictionary containing the filename and status of the upload.
    """
    file_content = await file.read()
    # Check if the uploaded file is a PNG or JPEG image
    file_type = imghdr.what(None, h=file_content)

    if file_type not in ["png", "jpeg", "jpg"]:
        return RedirectResponse("/user/profile?success=Supported file types are PNG/JPG/JPEG", status_code=status.HTTP_302_FOUND)

    user_id = request.session["USER_ID"]
    update_rsp = update_photo(user_id, file_content)
    if update_rsp:
        return RedirectResponse("/user/profile?success=Profile photo updated successfully", status_code=status.HTTP_302_FOUND)
    return RedirectResponse("/user/profile?error=Error updating profile photo", status_code=status.HTTP_302_FOUND)


@router.get("/settings", response_class=HTMLResponse)
async def settings_form(request: Request):
    """
    Display the user's image based on the user ID.

    Args:
        request (Request): The incoming request object.

    Returns:
        StreamingResponse: The streaming response containing the user's image.

    Raises:
        HTTPException: If the user's image is not found.
    """
    success = request.query_params.get("success", None)
    error = request.query_params.get("error", None)
    return templates.TemplateResponse("settings.html", 
                                      {"request": request,
                                       "success": success,
                                       "error": error})


@router.post("/update-credentials", response_class=HTMLResponse)
async def update_credentials(request: Request):
    """
    Handle the settings page for a user.

    Args:
        request (Request): The incoming request object.

    Returns:
        RedirectResponse: The response object for redirecting to a different page.
    """
    try:
        form = await request.form()
        old_password = form.get("old_password")
        password = form.get("password")
        repeat_password = form.get("repeat_password")

        user_id = request.session["USER_ID"]
        user = get_user_by_id(user_id)
        if not user:
            return RedirectResponse("/user/settings?error=Current passwords didn't match", status_code=status.HTTP_302_FOUND)
        if not PWD_CONTEXT.verify(old_password, user["password"]):
            return RedirectResponse("/user/settings?error=Current passwords didn't match", status_code=status.HTTP_302_FOUND)

        if password != repeat_password:
            return RedirectResponse("/user/settings?error=New password and confirm password didn't match", status_code=status.HTTP_302_FOUND)
        
        hashed_password = PWD_CONTEXT.hash(password)
        update_rsp = update_password(user_id, hashed_password)
        if update_rsp:
            return RedirectResponse("/user/settings?success=Password updated successfully", status_code=status.HTTP_302_FOUND)
        return RedirectResponse("/user/settings?error=Password update failed", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        print(e)
        return RedirectResponse("/user/settings?error=Something went wrong. Please try again later.", status_code=status.HTTP_302_FOUND)