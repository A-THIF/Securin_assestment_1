from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
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
