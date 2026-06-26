"""
Central configuration using pydantic-settings.
Reads from environment variables and .env file.
All config is accessed via: from config import settings
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # OpenRouter
    openrouter_api_key: str = Field(default="", env="OPENROUTER_API_KEY")
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    site_url: str = Field(default="http://localhost:8501", env="SITE_URL")
    site_name: str = Field(default="RAG SQL Agent", env="SITE_NAME")

    # Model defaults
    default_model: str = Field(default="openai/gpt-4o-mini", env="DEFAULT_MODEL")
    sql_generation_temperature: float = 0.05    # Low: we want deterministic SQL
    interpretation_temperature: float = 0.3     # Higher: more natural language

    # Agent behavior
    max_sql_retries: int = Field(default=3, env="MAX_RETRIES")
    max_rows_in_context: int = Field(default=50, env="MAX_ROWS_IN_CONTEXT")
    max_tokens_sql: int = 1000
    max_tokens_interpretation: int = 1500
    max_tokens_repair: int = 1000

    # RAG
    embedding_model: str = Field(default="all-MiniLM-L6-v2", env="EMBEDDING_MODEL")
    chroma_persist_dir: str = Field(default="./vector_store_db", env="CHROMA_PERSIST_DIR")
    schema_top_k: int = 5          # How many schema chunks to retrieve per query

    # Data loading
    max_preview_rows: int = 100
    max_file_size_mb: int = 200

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

# Available OpenRouter models (curated list)
AVAILABLE_MODELS = {
    "GPT-4o Mini (Fast & Cheap)":       "openai/gpt-4o-mini",
    "GPT-4o (Best OpenAI)":             "openai/gpt-4o",
    "Claude 3.5 Sonnet (Best Anthropic)":"anthropic/claude-3.5-sonnet",
    "Claude 3 Haiku (Ultra Fast)":      "anthropic/claude-3-haiku",
    "Gemini 1.5 Flash":                 "google/gemini-flash-1.5-8b",
    "Gemini 1.5 Pro":                   "google/gemini-1.5-pro",
    "Llama 3.1 70B Instruct":           "meta-llama/llama-3.1-70b-instruct",
    "Qwen 2.5 72B Instruct":            "qwen/qwen-2.5-72b-instruct",
}
