from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from api.routes import router
from core.database import engine
from models.model import Base

# Create tables
Base.metadata.create_all(bind=engine)

# ✅ Define app first
app = FastAPI()

# Templates folder
templates = Jinja2Templates(directory="templates")

# Include your API routes
app.include_router(router)

# Serve the frontend UI
@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/cves/{cve_id}/view", response_class=HTMLResponse)
def cve_detail_page(request: Request, cve_id: str):
    return templates.TemplateResponse("cve_detail.html", {"request": request, "cve_id": cve_id})

