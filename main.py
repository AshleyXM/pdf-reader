from fastapi import FastAPI, Path, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services.extract_workflow import extract_all_contents_from_pdf

import asyncio

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})  # context must include a "request" key


@app.get("/{pdf_url:path}")
def parse_pdf(pdf_url: str = Path(..., description="The URL of the PDF to process"),
              image: bool = Query(True, description="Whether to enable image extraction"),
              correct: bool = Query(True, description="Whether to enable text correction")):
    parsed_result = asyncio.run(extract_all_contents_from_pdf(pdf_url, image, correct))
    return parsed_result
