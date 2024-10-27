from pydantic import BaseModel

class SummarizeJobPostSchema(BaseModel):
    job_post_url: str