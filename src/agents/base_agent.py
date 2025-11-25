"""
Clase base para todos los agentes del sistema
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import config
from src.utils.rate_limiter import RateLimiter


class BaseAgent(ABC):
    """Clase base abstracta para agentes"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.llm = ChatGoogleGenerativeAI(
            model=config.MODEL_NAME,
            temperature=config.TEMPERATURE,
            google_api_key=config.GOOGLE_API_KEY
        )
        self.memory: Dict[str, Any] = {}
        # Rate limiter compartido para todas las instancias
        self.rate_limiter = RateLimiter()
    
    def _invoke_with_rate_limit(self, chain, inputs: Dict[str, Any]):
        """
        Invoca una cadena LLM con rate limiting automático
        
        Args:
            chain: Cadena LangChain a invocar
            inputs: Inputs para la cadena
            
        Returns:
            Resultado de la invocación
        """
        # Aplicar rate limiting antes de la llamada
        self.rate_limiter.wait_if_needed()
        
        try:
            result = chain.invoke(inputs)
            return result
        except Exception as e:
            # Manejar errores de rate limit específicamente
            error_str = str(e).lower()
            if "resourceexhausted" in error_str or "429" in error_str or "quota" in error_str:
                # Extraer tiempo de espera del error
                retry_after = None
                if "retry in" in error_str or "retry_delay" in error_str:
                    import re
                    numbers = re.findall(r'(\d+\.?\d*)', error_str)
                    if numbers:
                        retry_after = float(numbers[0])
                
                self.rate_limiter.handle_rate_limit_error(e, retry_after)
                # Reintentar después de esperar
                self.rate_limiter.wait_if_needed()
                return chain.invoke(inputs)
            else:
                # Re-lanzar otros errores
                raise
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa la entrada y devuelve un resultado
        
        Args:
            input_data: Datos de entrada para el agente
            
        Returns:
            Resultado del procesamiento
        """
        pass
    
    def update_memory(self, key: str, value: Any):
        """Actualiza la memoria del agente"""
        self.memory[key] = value
    
    def get_memory(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor de la memoria"""
        return self.memory.get(key, default)
    
    def clear_memory(self):
        """Limpia la memoria del agente"""
        self.memory.clear()
    
    def __str__(self):
        return f"{self.name} ({self.role})"

