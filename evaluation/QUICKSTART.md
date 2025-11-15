# 🚀 Guía Rápida - Evaluación AURA

## ⚡ Inicio Rápido (5 minutos)

### 1️⃣ Preparación

```bash
# 1. Asegúrate de tener el VectorStore procesado
#    (desde Streamlit -> Configuración -> Procesar Documentos)

# 2. Verifica que .env tiene GOOGLE_API_KEY configurada
```

### 2️⃣ Ejecutar Evaluación Completa

```bash
cd evaluation
python run_evaluation.py
```

Esto ejecutará:
- ✅ Tests del QuestionerAgent (8 escenarios)
- ✅ Tests del Sistema RAG (8 escenarios)  
- ✅ Tests End-to-End (8 escenarios)
- ✅ Generación de reporte HTML

**Tiempo estimado:** 10-15 minutos

### 3️⃣ Ver Resultados

```bash
# Abrir el reporte HTML generado
# Se guarda en: evaluation/results/report_TIMESTAMP.html
```

El reporte incluye:
- 📊 Métricas generales del sistema
- 🔍 Análisis detallado por componente
- 🎯 Scores de calidad LLM Judge
- ❌ Tests fallidos con detalles

---

## 🎯 Casos de Uso Comunes

### Solo Evaluar un Componente

```bash
# Solo QuestionerAgent (más rápido)
python run_evaluation.py -c questioner

# Solo RAG
python run_evaluation.py -c rag

# Solo Orchestrator (end-to-end)
python run_evaluation.py -c orchestrator
```

### Tests Individuales

```bash
# Test específico del QuestionerAgent
python test_questioner.py

# Test específico del RAG
python test_rag.py

# Test específico del Orchestrator
python test_orchestrator.py
```

### Generar Reporte desde JSON Existentes

```bash
python report_generator.py \
  results/questioner_20250111_120000.json \
  results/rag_20250111_120000.json \
  results/orchestrator_20250111_120000.json
```

---

## 📊 Interpretación Rápida

### Scores del Sistema

| Score | Estado | Significado |
|-------|--------|-------------|
| ≥ 90% | 🌟 EXCELENTE | Todo funciona perfectamente |
| 75-89% | ✅ BUENO | Sistema funcional, pequeñas mejoras posibles |
| 60-74% | ⚠️ ACEPTABLE | Funciona pero necesita optimización |
| < 60% | ❌ DEFICIENTE | Requiere atención urgente |

### Métricas Clave por Componente

**QuestionerAgent:**
- ✅ Precisión extracción > 85%
- ✅ Preguntas ≤ 5
- ✅ Score información > 60%

**RAG:**
- ✅ Tiempo búsqueda < 2s
- ✅ Relevancia > 70%
- ✅ VectorStore HEALTHY

**Orchestrator:**
- ✅ Tasa éxito > 90%
- ✅ Tiempo total < 30s
- ✅ Calidad LLM > 8/10

---

## 🔍 Solución de Problemas

### Error: VectorStore no encontrado

```bash
# Solución: Procesar documentos primero
# 1. Abre Streamlit: streamlit run app.py
# 2. Ve a Configuración -> Inicialización RAG
# 3. Haz clic en "Procesar Documentos"
```

### Error: GOOGLE_API_KEY no configurada

```bash
# Solución: Crear archivo .env
echo "GOOGLE_API_KEY=tu_api_key_aqui" > .env
```

### Tests muy lentos

```bash
# Reducir número de escenarios en test_scenarios.json
# O ejecutar componentes individualmente
python run_evaluation.py -c questioner  # Más rápido
```

### Error de importación

```bash
# Asegúrate de ejecutar desde el directorio correcto
cd evaluation
python run_evaluation.py

# Si persiste, verifica que estás en el entorno correcto
# Con uv:
uv sync
```

---

## 📁 Archivos Generados

Después de la evaluación, encontrarás:

```
evaluation/results/
├── questioner_TIMESTAMP.json      # Resultados QuestionerAgent
├── rag_TIMESTAMP.json             # Resultados RAG
├── orchestrator_TIMESTAMP.json    # Resultados Orchestrator
└── report_TIMESTAMP.html          # Reporte visual
```

**Recomendación:** Abre el archivo HTML para análisis visual completo.

---

## 💡 Tips Pro

### 1. Automatizar Evaluaciones

```bash
# Crear un cron job para evaluaciones periódicas
0 2 * * * cd /path/to/aura && python evaluation/run_evaluation.py
```

### 2. Comparar Resultados

```bash
# Guarda los JSON de diferentes fechas y compara métricas
python -c "
import json
with open('results/orchestrator_old.json') as f:
    old = json.load(f)
with open('results/orchestrator_new.json') as f:
    new = json.load(f)
print(f'Mejora: {new[\"success_rate\"] - old[\"success_rate\"]:.2%}')
"
```

### 3. CI/CD Integration

```yaml
# .github/workflows/evaluate.yml
name: AURA Evaluation
on: [push]
jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run evaluation
        run: python evaluation/run_evaluation.py
```

### 4. Custom Scenarios

```json
// Crea tus propios tests en datasets/test_scenarios.json
{
  "id": "my_test",
  "name": "Mi caso específico",
  "conversation": ["..."],
  "expected_extraction": {...}
}
```

---

## 🎓 Próximos Pasos

1. ✅ Ejecuta evaluación completa
2. 📊 Revisa reporte HTML
3. 🔍 Identifica áreas de mejora
4. 🛠️ Optimiza componentes débiles
5. 🔄 Re-evalúa para confirmar mejoras
6. 📈 Trackea métricas en el tiempo

---

## 📞 Soporte

¿Problemas? Revisa:
- 📖 [README completo](./README.md)
- 🔧 [Configuración](./config.py)
- 📊 Logs en consola durante ejecución

---

**¡Listo para evaluar tu sistema AURA! 🚀**

