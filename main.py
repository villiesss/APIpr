from fastapi import FastAPI, Response, Request
from fastapi.responses import PlainTextResponse, HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from driver import DB
from dispatcher import Dispatcher

dsp = Dispatcher()

e = DB.prerun_chk()
if not e:
    import sys
    sys.exit(f"Cannot connect to database. Programm shutting down...")

app = FastAPI()

@app.get("/api", response_class = HTMLResponse)
def index():
    html_content = '<h1>Hello from FastAPI</h1><br><br><a href="/help">Как работать с API?</a>'
    return html_content

@app.get("/api/request", response_class = JSONResponse)
def query_request(request: Request):
    query = request.query_params
    response = dsp.dispatch(query)
    return response