import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5433"))
    db_user: str = os.getenv("DB_USER", "construction_user")
    db_password: str = os.getenv("DB_PASSWORD", "ChangeThisPassword123!")
    db_name: str = os.getenv("DB_NAME", "construction_rag")

    # Ollama
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    llm_model: str = os.getenv("LLM_MODEL", "llama3.2:3b")

    # App
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8001"))
    debug: bool = os.getenv("DEBUG", "True").lower() in ("true", "1")

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()
