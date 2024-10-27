from pydantic_settings import BaseSettings

class Settings(BaseSettings): 
    API_PREFIX: str = "/api"
    GROQ_API_KEY:str
    ENV: str
    
    class Config:
        case_sensitive = True
        env_file = ".env"
    
    
settings = Settings()   