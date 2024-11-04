from typing import Union

from fastapi import FastAPI,__version__
from configuration.config import settings
from apis.api import api_router
from time import time
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


app = FastAPI(
    title="Job Post Info Backend API",
    version="v1",
    docs_url="/docs" if settings.ENV != "production" else None
    )

@app.get('/')
def hello_world():
    return "Hello,World"


@app.get('/ping')
async def hello():
    return {'res': 'pong', 'version': __version__, "time": time()}


app.include_router(api_router, prefix=settings.API_PREFIX)
