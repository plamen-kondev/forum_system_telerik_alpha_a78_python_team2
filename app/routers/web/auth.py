from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError
from app import config
from app.common.auth import AUTH_COOKIE_NAME, get_optional_user
from app.common.exceptions import UnauthorizedError, ConflictError
from app.common.templates import templates
from app.models.user import User, UserLogin, UserRegister
from app.services import auth_service


router = APIRouter(include_in_schema=False)

FIELD_HINTS = {
    "first_name": "First name must be 2 to 32 characters.",
    "last_name": "Last name must be 2 to 32 characters.",
    "email": "Enter a valid email address.",
    "username": "Username must be 2 to 16 characters: letters, numbers, _ or .",
    "password": "Password must be 8 to 72 characters.",
}

def _redirect_home_with_token(token: str)-> RedirectResponse:
    # 303 tells the browser to follow up with a GET, so refreshing the page won't resend the form
    response = RedirectResponse("/", status_code=303)
    # httpOnly, because javascript ne moje da chete cookie-ta, predpazvame token-a ot XSS
    # sameSite = lax -> znachi che cookie-to ne se prashta v requesti zapochnati ot drugi saitove

    response.set_cookie(
        AUTH_COOKIE_NAME,
        token,
        httponly = True,
        samesite = "lax",
        max_age = config.JWT_EXPIRE_MINUTES * 60,
    )
    return response

@router.get("/login", response_class=HTMLResponse)
def login_page(request:Request, user: User | None = Depends(get_optional_user)):
    if user:
        return RedirectResponse("/", status_code=303) #veche lognat
    return templates.TemplateResponse(request, "auth/login.html", {"user": None, "error": None, "username": ""})


@router.post("/login", response_class=HTMLResponse)
def login_submit(request: Request, username: str = Form(""), password: str = Form("")):
    try:
        token = auth_service.login(UserLogin(username=username, password=password))
    except UnauthorizedError as e:
        return templates.TemplateResponse(
            request, "auth/login.html",
            {"user": None, "error": e.message, "username": username},
            status_code = 400
        )
    return _redirect_home_with_token(token)


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request, user: User | None = Depends(get_optional_user)):
    if user:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(request, "auth/register.html", {"user": None, "errors": {}, "form": {}})



@router.post("/register", response_class=HTMLResponse)
def register_submit(
        request: Request,
        first_name: str = Form(""),
        last_name: str = Form(""),
        email: str = Form(""),
        username: str = Form(""),
        password: str = Form(""),
):
    # Values to put back into the form on error - never the password
    form = {"first_name": first_name, "last_name": last_name, "email": email, "username": username}
    errors: dict[str, str] = {}

    try:
        #sushtata validaciq kato v api-to
        data = UserRegister(first_name = first_name, last_name = last_name, email = email, username = username, password = password)
        user = auth_service.register(data)
    except ValidationError as e:
        #pydantic kazva koq chast e failnala i vrushtame hint na user-a
        for err in e.errors():
            field = str(err["loc"][0])
            errors[field] = FIELD_HINTS.get(field, err["msg"])
    except ConflictError as e:
        field = "username" if "Username" in e.message else "email"
        errors[field] = e.message
    if errors:
        return templates.TemplateResponse(
            request, "auth/register.html",
            {"user": None, "errors": errors, "form": form},
            status_code = 400
        )
    return _redirect_home_with_token(auth_service.create_access_token(user))


@router.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(AUTH_COOKIE_NAME)
    return response