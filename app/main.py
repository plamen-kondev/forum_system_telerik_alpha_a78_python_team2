from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import read_query

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

