from fastapi import FastAPI, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from extract_workflow import extract_all_contents_from_pdf

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})  # context must include a "request" key


@app.get("/{pdf_url:path}")
async def parse_pdf(request: Request, pdf_url: str = Path(..., description="The URL of the PDF to process")):
    print(pdf_url)
    parsed_pdf = extract_all_contents_from_pdf(pdf_url)
    return templates.TemplateResponse("parsed_pdf.html", {"request": request, "parsed_pdf": parsed_pdf})
