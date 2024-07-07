from fastapi import FastAPI, Path
from extract_workflow import extract_all_contents_from_pdf

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/{pdf_url:path}")
async def say_hello(pdf_url: str = Path(..., description="The URL of the PDF to process")):
    return extract_all_contents_from_pdf(pdf_url)
