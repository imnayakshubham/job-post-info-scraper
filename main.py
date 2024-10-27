from typing import Union

from fastapi import FastAPI
from configuration.config import settings
from apis.api import api_router


app = FastAPI()


app = FastAPI(
    title="Job Post Info Backend API",
    version="v1",
    docs_url="/docs" if settings.ENV != "production" else None
    )

app.include_router(api_router, prefix=settings.API_PREFIX)
