from fastapi import APIRouter
from apis.job_post_apis import job_post_apis

api_router = APIRouter()

api_router.include_router(job_post_apis.router,tags=["Job Post Summary"])
