"""
Configuración para el sistema de evaluación
"""
from pathlib import Path

# Directorios
EVALUATION_DIR = Path(__file__).parent
RESULTS_DIR = EVALUATION_DIR / "results"
DATASETS_DIR = EVALUATION_DIR / "datasets"

# Crear directorios si no existen
RESULTS_DIR.mkdir(exist_ok=True)
DATASETS_DIR.mkdir(exist_ok=True)

# Umbrales de calidad
THRESHOLDS = {
    "questioner": {
        "extraction_accuracy": 0.85,  # 85% precisión en extracción
        "max_questions": 5,
        "information_score_min": 60.0  # Score mínimo de información
    },
    "rag": {
        "precision_at_5": 0.80,  # 80% de precisión en top 5
        "recall_at_10": 0.70,    # 70% de recall en top 10
        "search_time_max": 2.0    # Máximo 2 segundos
    },
    "recommender": {
        "llm_judge_min_score": 8.0,  # Mínimo 8/10 en evaluación LLM
        "relevancia_min": 7.0,
        "diversidad_min": 6.0,
        "explicacion_min": 7.0
    },
    "orchestrator": {
        "success_rate": 0.90,     # 90% de tests exitosos
        "avg_time_max": 30.0,     # Máximo 30 segundos promedio
        "products_found_min": 1   # Al menos 1 producto
    }
}

# Configuración de LLM Judge
LLM_JUDGE_CONFIG = {
    "model": "gemini-2.5-flash-lite",
    "temperature": 0.1,  # Baja temperatura para evaluación consistente
    "max_retries": 3,
    "timeout": 30.0,  # Timeout de 30 segundos para llamadas LLM
    "request_timeout": 30.0  # Timeout de request HTTP
}

# Configuración de reportes
REPORT_CONFIG = {
    "format": "html",  # html, json, txt
    "include_detailed_traces": True,
    "save_artifacts": True
}

