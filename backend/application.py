from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse, Response
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
import torch
from io import BytesIO
import aiohttp
import asyncio
import urllib.request
import os
from fastai.vision import (load_learner, defaults, open_image)

origin="localhost:4200"

app = Starlette(debug=True)
app.add_middleware(CORSMiddleware, allow_headers=["*"], allow_origins=[origin, "*"], allow_methods=['*'],  allow_credentials=True)
defaults.device = torch.device('cpu')
path = Path.cwd()
file = 'model.pkl'
learner = load_learner(path, file)


@app.route("/")
def root(request):
    return HTMLResponse("Server up & running!")
    

@app.route("/classify-url", methods=["GET"])
async def classify_url(request):
    bytes = await get_bytes(request.query_params["url"])
    return predict_image_from_bytes(bytes)


@app.route("/upload", methods=["POST"])
async def upload(request):
    data = await request.form()
    bytes = await (data["file"].read())
    return predict_image_from_bytes(bytes)


def predict_image_from_bytes(bytes):
    img = open_image(BytesIO(bytes))
    _, _, losses = learner.predict(img)

    return JSONResponse({
        "predictions": sorted(
            zip(learner.data.classes, map(float, losses)),
            key=lambda p: p[1],
            reverse=True
        )
    })
    
async def get_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

def _build_cors_prelight_response():
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['content-type'] = 'application/json'
    response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT,DELETE"
    return response

def _build_cors_actual_response(response):
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 443))
    uvicorn.run(app, host='0.0.0.0', port=port)
