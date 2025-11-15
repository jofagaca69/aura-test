# 🧪 Sistema de Evaluación AURA

Sistema completo de evaluación para el sistema multi-agente AURA de recomendación de productos.

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Arquitectura](#arquitectura)
- [Componentes Evaluados](#componentes-evaluados)
- [Instalación](#instalación)
- [Uso](#uso)
- [Métricas y Umbrales](#métricas-y-umbrales)
- [Interpretación de Resultados](#interpretación-de-resultados)
- [Ejemplos](#ejemplos)

## 🎯 Descripción General

Este sistema de evaluación proporciona una suite completa para medir y validar el rendimiento de AURA a través de múltiples dimensiones:

- ✅ **Precisión de extracción de información** (QuestionerAgent)
- ✅ **Calidad de preguntas contextuales** (LLM-as-Judge)
- ✅ **Relevancia de búsqueda RAG** (VectorStore)
- ✅ **Calidad de recomendaciones** (LLM-as-Judge)
- ✅ **Rendimiento end-to-end** (Orchestrator)

## 🏗️ Arquitectura

```
evaluation/
├── __init__.py
├── config.py                    # Configuración y umbrales
├── llm_judge.py                # Evaluador LLM-as-Judge
├── test_questioner.py          # Tests del QuestionerAgent
├── test_rag.py                 # Tests del sistema RAG
├── test_orchestrator.py        # Tests end-to-end
├── report_generator.py         # Generador de reportes HTML
├── run_evaluation.py           # Script principal
├── datasets/
│   └── test_scenarios.json    # Escenarios de prueba
└── results/                    # Resultados generados
    ├── *.json                 # Resultados en JSON
    └── *.html                 # Reportes HTML
```

## 🔍 Componentes Evaluados

### 1. QuestionerAgent

**Evalúa:**
- Precisión de extracción de información estructurada
- Calidad y contextualidad de preguntas generadas
- Eficiencia (número de preguntas vs información obtenida)
- Score de completitud de información

**Métricas clave:**
```python
{
  "extraction_accuracy": 85%,      # Mínimo esperado
  "max_questions": 5,              # Máximo permitido
  "information_score_min": 60%     # Score mínimo de info
}
```

### 2. Sistema RAG

**Evalúa:**
- Velocidad de búsqueda en VectorStore
- Relevancia de documentos recuperados
- Salud del sistema (conectividad, diversidad)
- Precision@K y otras métricas de recuperación

**Métricas clave:**
```python
{
  "search_time_max": 2.0,          # Máximo 2 segundos
  "precision_at_5": 80%,           # Top 5 resultados
  "recall_at_10": 70%              # Top 10 resultados
}
```

### 3. Orchestrator (End-to-End)

**Evalúa:**
- Flujo completo de conversación
- Calidad de recomendaciones finales (LLM Judge)
- Tiempo total de ejecución
- Productos encontrados vs esperados
- Relevancia de recomendaciones

**Métricas clave:**
```python
{
  "success_rate": 90%,             # Tasa de éxito
  "avg_time_max": 30.0,           # Máximo 30 segundos
  "products_found_min": 1,         # Al menos 1 producto
  "llm_judge_min_score": 8.0      # Calidad mínima 8/10
}
```

## 🚀 Instalación

### Prerrequisitos

```bash
# Instalar dependencias (si usas uv)
uv sync

# O con pip
pip install langchain langchain-google-genai chromadb sentence-transformers
```

### Configuración

1. **Configurar variables de entorno:**
```bash
# .env
GOOGLE_API_KEY=your_key_here
```

2. **Verificar VectorStore:**
```bash
# Asegúrate de que el VectorStore está procesado
# Ve a la página de Configuración en Streamlit para procesar documentos
```

3. **Verificar escenarios de prueba:**
```bash
# Los escenarios están en evaluation/datasets/test_scenarios.json
# Puedes personalizarlos según tus necesidades
```

## 📖 Uso

### Evaluación Completa

Ejecutar todos los componentes:

```bash
python evaluation/run_evaluation.py
```

### Evaluación Selectiva

Evaluar componentes específicos:

```bash
# Solo QuestionerAgent
python evaluation/run_evaluation.py -c questioner

# Solo RAG
python evaluation/run_evaluation.py -c rag

# RAG + Orchestrator
python evaluation/run_evaluation.py -c rag orchestrator
```

### Evaluación Individual

Ejecutar tests de forma independiente:

```bash
# QuestionerAgent
python evaluation/test_questioner.py

# RAG
python evaluation/test_rag.py

# Orchestrator
python evaluation/test_orchestrator.py
```

### Generar Reporte desde Resultados Existentes

```bash
python evaluation/report_generator.py \
  evaluation/results/questioner_20250101_120000.json \
  evaluation/results/rag_20250101_120000.json \
  evaluation/results/orchestrator_20250101_120000.json
```

## 📊 Métricas y Umbrales

### Configuración de Umbrales

Edita `evaluation/config.py` para ajustar umbrales:

```python
THRESHOLDS = {
    "questioner": {
        "extraction_accuracy": 0.85,     # 85%
        "max_questions": 5,
        "information_score_min": 60.0
    },
    "rag": {
        "precision_at_5": 0.80,         # 80%
        "search_time_max": 2.0          # 2 segundos
    },
    "recommender": {
        "llm_judge_min_score": 8.0,     # 8/10
        "relevancia_min": 7.0,
        "diversidad_min": 6.0
    },
    "orchestrator": {
        "success_rate": 0.90,            # 90%
        "avg_time_max": 30.0,
        "products_found_min": 1
    }
}
```

### LLM-as-Judge

El evaluador LLM usa Gemini para juzgar calidad con 5 criterios:

1. **Relevancia (0-10):** ¿Los productos coinciden con necesidades?
2. **Diversidad (0-10):** ¿Hay variedad apropiada?
3. **Explicación (0-10):** ¿Las justificaciones son claras?
4. **Personalización (0-10):** ¿Se adaptó al contexto?
5. **Completitud (0-10):** ¿Se abordaron todos los criterios?

**Score total:** Promedio de los 5 criterios

## 📈 Interpretación de Resultados

### Formato de Resultados

Los resultados se guardan en dos formatos:

1. **JSON** (`evaluation/results/*.json`): Datos estructurados detallados
2. **HTML** (`evaluation/results/report_*.html`): Reporte visual interactivo

### Estructura de Resultados JSON

```json
{
  "component": "QuestionerAgent",
  "timestamp": "2025-01-01T12:00:00",
  "total_tests": 8,
  "successful_tests": 7,
  "success_rate": 0.875,
  "metrics": {
    "avg_extraction_accuracy": 87.5,
    "avg_questions_asked": 4.2,
    "avg_information_score": 75.3
  },
  "thresholds": { ... },
  "all_thresholds_passed": {
    "extraction_accuracy": true,
    "max_questions": true
  },
  "detailed_results": [ ... ]
}
```

### Interpretación de Scores

| Score | Interpretación | Acción |
|-------|---------------|--------|
| ≥ 90% | 🌟 EXCELENTE | Mantener calidad |
| 75-89% | ✅ BUENO | Pequeñas optimizaciones |
| 60-74% | ⚠️ ACEPTABLE | Revisar áreas débiles |
| < 60% | ❌ DEFICIENTE | Requiere mejoras urgentes |

### Reporte HTML

Abre el archivo HTML generado en un navegador para ver:

- 📊 **Resumen ejecutivo** con métricas generales
- 🔍 **Detalle por componente** con tablas y gráficos
- 📈 **Métricas de rendimiento** por escenario
- 🎯 **Análisis de calidad LLM Judge**
- ⚠️ **Tests fallidos** con detalles de error

## 💡 Ejemplos

### Ejemplo 1: Evaluación Completa

```bash
$ python evaluation/run_evaluation.py

================================================================================
🚀 SUITE DE EVALUACIÓN AURA
================================================================================
📅 Timestamp: 20250111_143022
🔧 Configurando entorno...
   ✅ Configuración validada
   📚 Cargando VectorStore...
   ✅ VectorStore cargado

================================================================================
🧪 FASE 1: Evaluación del QuestionerAgent
================================================================================
...
Tests ejecutados: 8
Tests exitosos: 7 (87.5%)

================================================================================
🧪 FASE 2: Evaluación del Sistema RAG
================================================================================
...
Tests ejecutados: 8
Tests exitosos: 7 (87.5%)

================================================================================
🧪 FASE 3: Evaluación End-to-End del Orchestrator
================================================================================
...
Tests ejecutados: 8
Tests exitosos: 6 (75.0%)

================================================================================
📊 RESUMEN FINAL DE EVALUACIÓN
================================================================================
🎯 SCORE GENERAL DEL SISTEMA: 83.3%
   ✅ BUENO - Sistema funcionando correctamente

📁 Archivos generados:
   - Resultados JSON: evaluation/results/*_20250111_143022.json
   - Reporte HTML: evaluation/results/report_20250111_143022.html
```

### Ejemplo 2: Test Unitario de QuestionerAgent

```python
from evaluation.test_questioner import QuestionerEvaluator, load_scenarios

# Cargar escenarios
scenarios = load_scenarios()

# Crear evaluador
evaluator = QuestionerEvaluator()

# Ejecutar un escenario específico
result = evaluator.test_scenario(scenarios[0])

print(f"Precisión: {result['extraction_evaluation']['accuracy_percentage']:.1f}%")
print(f"Preguntas: {result['questions_asked']}")
print(f"Éxito: {result['overall_success']}")
```

### Ejemplo 3: Evaluación Custom con Escenarios Propios

```python
import json
from evaluation.test_orchestrator import OrchestratorEvaluator
from src.rag.vector_store import VectorStore

# Cargar VectorStore
vector_store = VectorStore()
vector_store.load_vectorstore()

# Crear evaluador
evaluator = OrchestratorEvaluator(vector_store)

# Definir escenario custom
custom_scenario = {
    "id": "custom_1",
    "name": "Test personalizado",
    "category": "laptop",
    "difficulty": "medium",
    "conversation": [
        "Busco una laptop",
        "Para trabajo de oficina",
        "Hasta 800 euros",
        "Que sea ligera",
        "Sin preferencias de marca"
    ],
    "expected_extraction": {
        "categoria_producto": "laptop",
        "presupuesto_max": 800.0,
        "uso_principal": "trabajo de oficina",
        "caracteristicas_clave": ["ligera"]
    },
    "expected_outcome": {
        "should_find_products": True,
        "min_products": 1,
        "max_questions": 5,
        "relevance_keywords": ["laptop", "oficina", "ligera"]
    }
}

# Ejecutar test
result = evaluator.test_scenario(custom_scenario)

# Ver resultados
print(json.dumps(result, indent=2, ensure_ascii=False))
```

## 🔧 Personalización

### Añadir Nuevos Escenarios de Prueba

Edita `evaluation/datasets/test_scenarios.json`:

```json
{
  "scenarios": [
    {
      "id": "my_scenario",
      "name": "Mi escenario personalizado",
      "category": "producto",
      "difficulty": "medium",
      "conversation": [
        "Primera respuesta del usuario",
        "Segunda respuesta",
        ...
      ],
      "expected_extraction": {
        "categoria_producto": "laptop",
        "presupuesto_max": 1000.0,
        ...
      },
      "expected_outcome": {
        "should_find_products": true,
        "min_products": 1,
        "relevance_keywords": ["keyword1", "keyword2"]
      }
    }
  ]
}
```

### Modificar Prompts de LLM Judge

Edita los prompts en `evaluation/llm_judge.py` para ajustar criterios de evaluación.

### Crear Evaluadores Custom

```python
from evaluation.llm_judge import LLMJudge
from src.agents.base_agent import BaseAgent

class MyCustomEvaluator:
    def __init__(self):
        self.llm_judge = LLMJudge()
    
    def evaluate_custom_metric(self, data):
        # Tu lógica de evaluación
        pass
```

## 📚 Referencias

- **LangChain Documentation:** https://python.langchain.com/
- **Google Gemini:** https://ai.google.dev/
- **LangSmith (Tracing):** https://smith.langchain.com/
- **ChromaDB:** https://www.trychroma.com/

## 🤝 Contribuciones

Para añadir nuevas evaluaciones o mejorar las existentes:

1. Crea nuevos escenarios de prueba en `datasets/`
2. Añade evaluadores específicos siguiendo el patrón existente
3. Actualiza umbrales en `config.py` según necesidad
4. Documenta nuevas métricas en este README

## 📝 Notas Importantes

⚠️ **Consideraciones:**

- Los tests con LLM Judge pueden tardar varios minutos
- Los costos de API aumentan con más tests (usa Gemini Flash para reducir costos)
- Los resultados pueden variar ligeramente entre ejecuciones debido a la naturaleza no determinística de los LLMs
- Asegúrate de tener suficientes datos en el VectorStore antes de evaluar

🎯 **Mejores Prácticas:**

- Ejecuta evaluaciones en entorno de desarrollo antes de producción
- Mantén un historial de resultados para tracking de mejoras
- Revisa tests fallidos individualmente para entender causas raíz
- Ajusta umbrales según tu caso de uso específico

---

**Creado por:** José Fabián García Camargo
**Versión:** 1.0
**Fecha:** Noviembre 2025

