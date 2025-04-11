import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration settings
class Config:
    # Ollama configuration
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3')
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')

    # Database configuration
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database', 'job_screening.db')

    # Matching threshold
    MATCH_THRESHOLD = 0.8  # 80% match required

    # Embedding model configuration
    EMBEDDING_MODEL = 'all-MiniLM-L6-v2'

    # API Key configuration
    API_KEY = os.getenv("Bearer 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")