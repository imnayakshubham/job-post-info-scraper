from pydantic import BaseModel

class SummarizeJobPostSchema(BaseModel):
    job_post_url: str
    
    
    
class RandomQuestionsSchema(BaseModel):
    topic: str
    complexity_level: str = "easy"