from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

home = APIRouter()


@home.get("/")
async def home_page(request: Request):
    """
    Home Page - Redirects to docs
    """
    return RedirectResponse("/docs")
