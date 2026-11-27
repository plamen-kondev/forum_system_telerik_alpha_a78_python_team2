from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from app.common.auth import get_optional_user
from app.common.templates import templates
from app.models.user import User
from app.services import stats_service

#False -> da ne se pokazvat html stranicite v swagger-a
router = APIRouter(include_in_schema=False)

@router.get("/",response_class = HTMLResponse)
def home(request: Request, user: User | None = Depends(get_optional_user)):
    #user e None za anonymous posetiteli znachi template-a shte pokaje login/register
    return templates.TemplateResponse(request, "home.html",
                                      {
                                          "user": user,
                                          "stats": stats_service.get_home_stats(),
                                          "categories": stats_service.get_categories(),
                                      },
                                      )


