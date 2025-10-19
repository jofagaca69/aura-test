# 🤖 Sistema Dinámico de AURA

## ✨ Nueva Funcionalidad: Preguntas Generadas por LLM

El sistema AURA ahora usa **inteligencia artificial para generar preguntas dinámicamente** en lugar de usar preguntas predefinidas.

## 🔄 Diferencias entre Sistema Original vs Dinámico

### ❌ Sistema Original (Predefinido)
```
AURA: ¿Cuál es tu presupuesto aproximado para esta compra?
Usuario: 1000 dólares

AURA: ¿Qué tipo de producto estás buscando? (categoría)
Usuario: Una laptop

AURA: ¿Qué características son más importantes para ti?
Usuario: RAM y procesador

AURA: ¿Tienes alguna marca o especificación preferida?
Usuario: Dell

AURA: ¿Para qué uso principal necesitas este producto?
```

**Problemas:**
- ❌ Preguntas fijas, no se adaptan
- ❌ Siempre hace las mismas 5 preguntas
- ❌ No considera el contexto de respuestas anteriores
- ❌ Puede hacer preguntas redundantes

### ✅ Sistema Dinámico (Con LLM)

```
AURA: 👋 ¡Hola! Soy AURA, tu asistente inteligente de recomendaciones.
      ¿Qué tipo de producto estás buscando hoy?

Usuario: Necesito algo para trabajar desde casa

AURA: Entiendo que necesitas algo para trabajar desde casa. 
      ¿Podrías ser más específico? ¿Buscas una computadora, 
      un escritorio, una silla ergonómica, o algo más?

Usuario: Una computadora portátil

AURA: Perfecto, una laptop para trabajo remoto. 
      ¿Cuál es tu presupuesto aproximado?

Usuario: Hasta 1500 dólares

AURA: Excelente. ¿Qué tipo de trabajo realizas? Por ejemplo, 
      ¿programación, diseño gráfico, videollamadas, o uso general?

Usuario: Principalmente programación con Docker y VMs

AURA: Entiendo, necesitas bastante potencia. ¿Viajas frecuentemente 
      o la usarás principalmente en un lugar fijo? Esto me ayuda 
      a evaluar la importancia del peso y la batería.

Usuario: Viajo ocasionalmente

AURA: [Analiza que ya tiene suficiente información y procede]
      ✨ ¡Perfecto! He analizado toda nuestra conversación...
```

**Ventajas:**
- ✅ Preguntas adaptadas al contexto
- ✅ Conversación natural y fluida
- ✅ Detecta automáticamente cuándo tiene suficiente información
- ✅ No hace preguntas redundantes
- ✅ Puede pedir aclaraciones cuando algo no está claro
- ✅ Se adapta al estilo de respuesta del usuario

## 🧠 Cómo Funciona Internamente

### Flujo del Sistema Dinámico

```
┌─────────────────────────────────────────────────────────┐
│  1. INICIO DE CONVERSACIÓN                              │
├─────────────────────────────────────────────────────────┤
│  DynamicInformationCollectorAgent                       │
│  - Genera primera pregunta con LLM                      │
│  - Considera: contexto vacío, objetivo general          │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  2. USUARIO RESPONDE                                    │
├─────────────────────────────────────────────────────────┤
│  - Respuesta se añade al historial                      │
│  - LLM extrae información estructurada                  │
│  - Actualiza: presupuesto, categoría, características   │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  3. GENERACIÓN DE SIGUIENTE PREGUNTA                    │
├─────────────────────────────────────────────────────────┤
│  LLM analiza:                                           │
│  ✓ Información ya recopilada                            │
│  ✓ Historial de conversación                            │
│  ✓ Qué información falta                                │
│  ✓ Contexto de la última respuesta                      │
│                                                          │
│  Genera pregunta específica y contextual                │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  4. EVALUACIÓN DE SUFICIENCIA                           │
├─────────────────────────────────────────────────────────┤
│  ¿Tenemos suficiente información?                       │
│  - Presupuesto: ✓                                       │
│  - Categoría: ✓                                         │
│  - Uso principal: ✓                                     │
│  - Características clave: ✓                             │
│                                                          │
│  SI → Proceder a recomendaciones                        │
│  NO → Repetir desde paso 2                              │
└─────────────────────────────────────────────────────────┘
```

### Información que Rastrea

```python
information_gathered = {
    'presupuesto': "1200-1500 dólares",
    'categoria': "Laptop",
    'caracteristicas': ["16GB RAM", "Procesador potente", "Portátil"],
    'uso_principal': "Programación con Docker y VMs",
    'preferencias_marca': "Dell preferido, abierto a otras",
    'prioridades': ["Rendimiento", "Portabilidad"],
    'restricciones': ["Viaja ocasionalmente"]
}
```

## 📊 Comparación de Resultados

### Ejemplo 1: Usuario Claro

**Sistema Predefinido:**
- 5 preguntas fijas
- 5 respuestas del usuario
- Total: 10 intercambios

**Sistema Dinámico:**
- 3-4 preguntas adaptadas
- Detecta información completa antes
- Total: 6-8 intercambios ✅ Más eficiente

### Ejemplo 2: Usuario Vago

**Sistema Predefinido:**
```
AURA: ¿Cuál es tu presupuesto?
Usuario: No sé, algo normal
AURA: ¿Qué tipo de producto buscas?
Usuario: Algo para la casa
[Continúa sin aclarar]
```

**Sistema Dinámico:**
```
AURA: ¿Cuál es tu presupuesto?
Usuario: No sé, algo normal
AURA: Entiendo. ¿Podrías darme un rango aproximado? 
      Por ejemplo, ¿menos de $500, entre $500-$1000, 
      o más de $1000?
Usuario: Entre 500 y 1000
[El LLM pide aclaraciones cuando es necesario] ✅
```

## 🎯 Ventajas Clave

### 1. Adaptabilidad
```python
# Si el usuario menciona múltiples cosas en una respuesta
Usuario: "Necesito una laptop de 1200 dólares para programar"

# Sistema dinámico extrae:
- Categoría: Laptop ✓
- Presupuesto: 1200 dólares ✓
- Uso: Programación ✓

# Siguiente pregunta se adapta:
AURA: "¿Qué lenguajes de programación usas principalmente 
       y necesitas ejecutar entornos virtuales o contenedores?"
```

### 2. Detección de Información Suficiente
```python
def is_information_sufficient():
    # Verifica campos críticos
    has_budget = information_gathered['presupuesto'] is not None
    has_category = information_gathered['categoria'] is not None
    has_use = information_gathered['uso_principal'] is not None
    
    # O máximo de preguntas alcanzado
    return (has_budget and has_category) or questions_asked >= 7
```

### 3. Contexto Conversacional
```python
# El LLM recibe en cada pregunta:
prompt = f"""
INFORMACIÓN YA RECOPILADA:
{information_gathered}

CONVERSACIÓN HASTA AHORA:
{conversation_history}

ÚLTIMA RESPUESTA DEL USUARIO:
{user_response}

Genera la siguiente pregunta más relevante...
"""
```

## 🚀 Cómo Usar el Sistema Dinámico

### Opción 1: Usar main.py (Ya Configurado)
```bash
uv run python main.py
```

El sistema ahora usa automáticamente el agente dinámico.

### Opción 2: Usar Programáticamente
```python
from src.rag.vector_store import VectorStore
from src.orchestrator_dynamic import DynamicMultiAgentOrchestrator

# Cargar vectorstore
vector_store = VectorStore()
vector_store.load_vectorstore()

# Crear orquestador dinámico
orchestrator = DynamicMultiAgentOrchestrator(vector_store)

# Iniciar sesión
greeting = orchestrator.start_session()
print(greeting)

# Procesar respuestas
response = orchestrator.process_user_input("Busco una laptop")
print(response['message'])
```

## ⚙️ Configuración

### Ajustar Número Máximo de Preguntas

```python
# En src/agents/dynamic_collector.py
self.max_questions = 7  # Cambiar este valor
```

### Modificar Criterios de Suficiencia

```python
# En src/agents/dynamic_collector.py
def is_information_sufficient(self):
    # Personalizar lógica
    critical_fields = ['categoria', 'presupuesto', 'uso_principal']
    has_critical = all(self.information_gathered.get(field) 
                      for field in critical_fields)
    return has_critical
```

## 📝 Notas Importantes

### Límites de API
El sistema dinámico hace **más llamadas al LLM**:
- 1 llamada por cada pregunta generada
- 1 llamada para extraer información
- 1 llamada para análisis final

**Solución**: El sistema tiene reintentos automáticos y maneja los límites de cuota.

### Latencia
- Primera pregunta: ~2-3 segundos
- Preguntas subsecuentes: ~2-3 segundos cada una
- Más lento que preguntas predefinidas, pero **mucho más inteligente**

### Calidad de Conversación
Depende del modelo LLM usado:
- `gemini-1.5-flash`: Rápido, buena calidad ✅
- `gemini-1.5-pro`: Más lento, excelente calidad ⭐
- `gemini-2.5-flash`: Balance óptimo (actual) ⚡

## 🎓 Ejemplos de Conversaciones Reales

### Conversación 1: Usuario Experimentado
```
AURA: ¿Qué producto estás buscando?
Usuario: MacBook Pro M3 o similar, presupuesto 2500

AURA: Entiendo, buscas laptops de alto rendimiento. 
      ¿Para qué uso específico? ¿Desarrollo, diseño, video?
Usuario: Desarrollo iOS y machine learning

AURA: Perfecto. ¿Necesitas GPU dedicada o la GPU integrada 
      del M3 es suficiente para tus modelos de ML?
[Solo 3 preguntas, muy específicas] ✅
```

### Conversación 2: Usuario Novato
```
AURA: ¿Qué producto estás buscando?
Usuario: No sé, algo para estudiar

AURA: Entiendo. ¿Estudias en línea o presencial? 
      ¿Necesitas algo portátil o para usar en casa?
Usuario: En línea, desde mi cuarto

AURA: Perfecto. ¿Qué programas o aplicaciones usas 
      principalmente? ¿Navegador, Office, algo más?
[Guía al usuario paso a paso] ✅
```

## 🔧 Troubleshooting

### "Muchas preguntas"
Reduce `max_questions` en `dynamic_collector.py`

### "Preguntas no relevantes"
Mejora el prompt del sistema en `generate_next_question()`

### "Error de cuota"
Espera unos minutos o cambia a un modelo con mayor cuota

## 📚 Archivos Relacionados

- `src/agents/dynamic_collector.py` - Agente dinámico
- `src/orchestrator_dynamic.py` - Orquestador dinámico
- `main.py` - Usa sistema dinámico por defecto
- `test_dynamic.py` - Pruebas del sistema

---

**¡El sistema dinámico está activo! Ejecuta `python main.py` para probarlo.** 🚀

