"""
Configuración del sistema AURA
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración centralizada del sistema"""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Modelo
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # RAG
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))
    
    # Directorios
    DATA_DIR = "data"
    PRODUCTS_DIR = os.path.join(DATA_DIR, "products")
    CHROMA_DIR = os.path.join(DATA_DIR, "chroma_db")
    
    @classmethod
    def validate(cls):
        """Valida que la configuración esté completa"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY no está configurada. "
                "Por favor, crea un archivo .env basado en .env.example"
            )


config = Config()

