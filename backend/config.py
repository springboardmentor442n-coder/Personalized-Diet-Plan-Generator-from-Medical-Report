import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    OCR_MODEL: str = "meta-llama/llama-4-maverick-17b-128e-instruct"
    DIET_MODEL: str = "llama-3.1-8b-instant"

settings = Settings()
