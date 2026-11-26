from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.database import read_query
from fastapi.responses import JSONResponse
from app.database import read_query
from app.common.exceptions import AppError
from app.routers.api import auth as auth_api
from app.routers.api import topics as topics_api
from app.routers.api import replies as replies_api
from app.routers.api import reply_votes as reply_votes_api


app = FastAPI(
    title="Hot Takes API",
    description="A forum for unpopular opinions. Challenge opinions, not people.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/health", tags=["System"])
def health():
    try:
        read_query("SELECT 1")
        db_status = "ok"
    except Exception:
        db_status = "unreachable"
    return {"status": "ok", "database": db_status}

@app.exception_handler(AppError)
def handle_app_error(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

app.include_router(auth_api.router)
app.include_router(topics_api.router)
app.include_router(replies_api.router)
app.include_router(reply_votes_api.router)
