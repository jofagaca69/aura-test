"""
Rate limiter para controlar las llamadas a la API de Gemini
Evita exceder los límites de cuota (15 requests/minuto en tier gratuito)
"""
import time
import threading
from typing import Optional
from collections import deque


class RateLimiter:
    """
    Rate limiter thread-safe para controlar llamadas a la API
    
    Implementa token bucket algorithm para respetar límites de cuota
    """
    
    _instance: Optional['RateLimiter'] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern para compartir el rate limiter entre todas las instancias"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Inicializa el rate limiter"""
        if self._initialized:
            return
        
        # Configuración para tier gratuito de Gemini
        # 15 requests por minuto = 1 request cada 4 segundos (con margen de seguridad)
        self.max_requests_per_minute = 12  # Usar 12 para tener margen de seguridad
        self.min_delay_between_requests = 60.0 / self.max_requests_per_minute  # ~5 segundos
        
        # Historial de requests (timestamps)
        self.request_times: deque = deque(maxlen=self.max_requests_per_minute)
        self.lock = threading.Lock()
        
        self._initialized = True
    
    def wait_if_needed(self):
        """
        Espera si es necesario para respetar el rate limit
        
        Calcula cuánto tiempo esperar basado en el historial de requests
        """
        with self.lock:
            now = time.time()
            
            # Limpiar requests antiguos (más de 1 minuto)
            while self.request_times and (now - self.request_times[0]) > 60.0:
                self.request_times.popleft()
            
            # Si ya alcanzamos el límite, esperar
            if len(self.request_times) >= self.max_requests_per_minute:
                # Calcular cuánto esperar hasta que expire el request más antiguo
                oldest_request = self.request_times[0]
                wait_time = 60.0 - (now - oldest_request) + 0.5  # +0.5s de margen
                
                if wait_time > 0:
                    print(f"⏳ Rate limit: esperando {wait_time:.1f}s para respetar cuota de API...")
                    time.sleep(wait_time)
                    # Limpiar el historial después de esperar
                    now = time.time()
                    self.request_times.clear()
            
            # Asegurar delay mínimo entre requests
            if self.request_times:
                last_request = self.request_times[-1]
                time_since_last = now - last_request
                if time_since_last < self.min_delay_between_requests:
                    wait_time = self.min_delay_between_requests - time_since_last
                    if wait_time > 0:
                        time.sleep(wait_time)
                        now = time.time()
            
            # Registrar este request
            self.request_times.append(now)
    
    def handle_rate_limit_error(self, error: Exception, retry_after: Optional[float] = None):
        """
        Maneja errores de rate limit (429) de la API
        
        Args:
            error: La excepción recibida
            retry_after: Tiempo sugerido para reintentar (en segundos)
        """
        error_str = str(error).lower()
        
        # Extraer tiempo de espera sugerido del error si está disponible
        if retry_after is None:
            # Intentar extraer del mensaje de error
            if "retry in" in error_str or "retry_delay" in error_str:
                # Buscar números en el mensaje
                import re
                numbers = re.findall(r'(\d+\.?\d*)', error_str)
                if numbers:
                    retry_after = float(numbers[0])
        
        wait_time = retry_after or 30.0  # Default: 30 segundos
        
        print(f"⚠️ Rate limit excedido. Esperando {wait_time:.1f}s antes de reintentar...")
        time.sleep(wait_time)
        
        # Limpiar historial para empezar fresco
        with self.lock:
            self.request_times.clear()
    
    def reset(self):
        """Resetea el historial de requests (útil para testing)"""
        with self.lock:
            self.request_times.clear()


def rate_limit_decorator(func):
    """
    Decorador para aplicar rate limiting automáticamente a funciones que llaman a la API
    """
    def wrapper(*args, **kwargs):
        limiter = RateLimiter()
        limiter.wait_if_needed()
        return func(*args, **kwargs)
    return wrapper

