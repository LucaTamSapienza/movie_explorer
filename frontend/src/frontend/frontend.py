from fastapi import FastAPI, Request, Query, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import os

app = FastAPI()

# Set up the static files directory for CSS and images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up the Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# Retrive the backend URL from environment variables (inside docker) or use a default value (outside docker)
BASE_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8003")

# homepage endpoint
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# schema endpoint
@app.get("/schema", response_class=HTMLResponse)
async def schema_summary(request: Request):
    try:
        response = requests.get(f"{BASE_URL}/schema_summary")
        schema = response.json()
    except Exception as e:
        schema = [{"table_name": "Errore", "column_name": str(e)}]
    
    return templates.TemplateResponse("schema.html", {"request": request, "schema": schema})

# search_form page, just for good UX
@app.get("/form_search", response_class=HTMLResponse)
async def search_page(request: Request):
    return templates.TemplateResponse("form_search.html", {"request": request})

# search endpoint
@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, question: str = Query(...)):
    import urllib.parse
    try:
        encoded_question = urllib.parse.quote(question)
        response = requests.get(f"{BASE_URL}/search/{encoded_question}")
        if response.status_code == 422:
            # Mostra il messaggio di errore del backend
            detail = response.json().get("detail", "Domanda non supportata.")
            result = [{"item_type": "Errore", "properties": [{"property_name": "errore", "property_value": detail}]}]
        else:
            result = response.json()
    except Exception as e:
        result = [{"item_type": "Errore", "properties": [{"property_name": "errore", "property_value": str(e)}]}]
    
    return templates.TemplateResponse("search_result.html", {"request": request, "result": result, "question": question})


# add_form page, just for good UX
@app.get("/form_add", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form_add.html", {"request": request})

# add endpoint
@app.post("/add", response_class=HTMLResponse)
async def add(request: Request, data_line: str = Form(...)):
    try:
        response = requests.post(f"{BASE_URL}/add", json={"data_line": data_line})
        if response.status_code == 422:
            # Mostra il messaggio di errore del backend
            detail = response.json().get("detail", "Errore nell'inserimento.")
            result = {"status": "errore", "message": detail}
        else:
            result = response.json()
    except Exception as e:
        result = {"status": "errore", "message": str(e)}

    return templates.TemplateResponse("add_result.html", {"request": request, "result": result})

