# 🚀 Comandos Útiles - Sistema de Evaluación AURA

## 📋 Comandos Rápidos

### Evaluación Completa
```bash
# Ejecutar toda la suite de evaluación
python evaluation/run_evaluation.py

# Ver resultados
cd evaluation/results
# Abrir el archivo HTML más reciente en navegador
```

### Evaluaciones Selectivas
```bash
# Solo QuestionerAgent (más rápido, ~3 min)
python evaluation/run_evaluation.py -c questioner

# Solo RAG
python evaluation/run_evaluation.py -c rag

# Solo Orchestrator (end-to-end)
python evaluation/run_evaluation.py -c orchestrator

# RAG + Orchestrator
python evaluation/run_evaluation.py -c rag orchestrator
```

### Tests Individuales
```bash
# QuestionerAgent
python evaluation/test_questioner.py

# Sistema RAG
python evaluation/test_rag.py

# Orchestrator E2E
python evaluation/test_orchestrator.py
```

### Ejemplos Prácticos
```bash
# Ver todos los ejemplos disponibles
python evaluation/examples.py

# Ejecutar ejemplo específico
python evaluation/examples.py 1  # QuestionerAgent
python evaluation/examples.py 2  # RAG búsqueda custom
python evaluation/examples.py 3  # E2E custom
python evaluation/examples.py 4  # LLM Judge directo (más rápido)
python evaluation/examples.py 5  # Comparar versiones
```

---

## 📊 Ver Resultados

### Listar Resultados Recientes
```bash
# Windows PowerShell
ls evaluation/results/*.json | Sort-Object LastWriteTime -Descending | Select-Object -First 5

# Linux/Mac
ls -lt evaluation/results/*.json | head -5
```

### Abrir Reporte HTML Más Reciente
```bash
# Windows
start evaluation/results/report_*.html

# Linux
xdg-open evaluation/results/report_*.html

# Mac
open evaluation/results/report_*.html
```

### Ver Resumen de un Resultado JSON
```bash
# Windows PowerShell
python -c "import json; data=json.load(open('evaluation/results/orchestrator_TIMESTAMP.json')); print(f'Tasa éxito: {data[\"success_rate\"]*100:.1f}%')"

# Linux/Mac
python3 -c "import json; data=json.load(open('evaluation/results/orchestrator_TIMESTAMP.json')); print(f'Tasa éxito: {data[\"success_rate\"]*100:.1f}%')"
```

---

## 🔧 Personalización

### Editar Escenarios de Prueba
```bash
# Abrir en editor
code evaluation/datasets/test_scenarios.json
# o
notepad evaluation/datasets/test_scenarios.json
```

### Modificar Umbrales
```bash
# Editar configuración
code evaluation/config.py
```

### Ajustar Prompts LLM Judge
```bash
# Editar evaluador
code evaluation/llm_judge.py
```

---

## 🐍 Uso desde Python

### Evaluación Programática
```python
# evaluation_script.py
from evaluation.run_evaluation import AURAEvaluationSuite
from src.rag.vector_store import VectorStore

# Cargar VectorStore
vector_store = VectorStore()
vector_store.load_vectorstore()

# Crear suite
suite = AURAEvaluationSuite(vector_store)

# Ejecutar evaluación
suite.run_all(components=['questioner', 'rag'])

# Acceder a resultados
print(suite.results)
```

### Test Específico
```python
from evaluation.test_questioner import QuestionerEvaluator, load_scenarios

scenarios = load_scenarios()
evaluator = QuestionerEvaluator()

# Test un escenario
result = evaluator.test_scenario(scenarios[0])
print(f"Éxito: {result['overall_success']}")
```

### LLM Judge Directo
```python
from evaluation.llm_judge import LLMJudge

judge = LLMJudge()
result = judge.evaluate_recommendations(
    user_analysis="Usuario busca laptop para gaming",
    search_criteria="Presupuesto: 1500€, GPU potente",
    recommendations="1. ASUS ROG...\n2. MSI...",
    products_found=2
)

if result['success']:
    print(f"Score: {result['evaluation']['score_total']}/10")
```

---

## 📈 Análisis de Resultados

### Comparar Dos Evaluaciones
```python
import json

# Cargar resultados
with open('evaluation/results/orchestrator_old.json') as f:
    old = json.load(f)
with open('evaluation/results/orchestrator_new.json') as f:
    new = json.load(f)

# Comparar
print(f"Tasa éxito:")
print(f"  Antes: {old['success_rate']*100:.1f}%")
print(f"  Ahora: {new['success_rate']*100:.1f}%")
print(f"  Mejora: {(new['success_rate']-old['success_rate'])*100:+.1f}%")
```

### Extraer Métricas Específicas
```python
import json
from pathlib import Path

# Buscar todos los resultados de orchestrator
results_dir = Path('evaluation/results')
files = sorted(results_dir.glob('orchestrator_*.json'))

# Extraer scores LLM Judge
llm_scores = []
for file in files:
    with open(file) as f:
        data = json.load(f)
        score = data['metrics']['llm_judge_scores']['avg']
        llm_scores.append((file.stem, score))

# Imprimir evolución
for name, score in llm_scores:
    print(f"{name}: {score:.1f}/10")
```

---

## 🔄 Automatización

### Script de Evaluación Periódica
```bash
#!/bin/bash
# evaluate_daily.sh

cd /path/to/aura-test/aura-test
python evaluation/run_evaluation.py

# Enviar notificación (opcional)
echo "Evaluación completada" | mail -s "AURA Evaluation" you@email.com
```

### Cron Job (Linux/Mac)
```bash
# Ejecutar evaluación diaria a las 2 AM
0 2 * * * cd /path/to/aura && python evaluation/run_evaluation.py >> /var/log/aura_eval.log 2>&1
```

### Task Scheduler (Windows)
```powershell
# Crear tarea programada
$action = New-ScheduledTaskAction -Execute "python" -Argument "evaluation/run_evaluation.py" -WorkingDirectory "C:\path\to\aura"
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "AURA Evaluation"
```

---

## 🐛 Debug y Troubleshooting

### Modo Verbose
```python
# Agregar prints detallados en los evaluadores
# Editar test_*.py y descomentar prints de debug
```

### Ver Trazas Completas
```python
# Ejecutar con traceback completo
import traceback
try:
    evaluator.run_all_tests(scenarios)
except Exception as e:
    traceback.print_exc()
```

### Test con un Solo Escenario
```python
from evaluation.test_orchestrator import OrchestratorEvaluator
from src.rag.vector_store import VectorStore

vector_store = VectorStore()
vector_store.load_vectorstore()

evaluator = OrchestratorEvaluator(vector_store)

# Crear escenario mínimo para debug
test_scenario = {
    "id": "debug_test",
    "name": "Debug test",
    "category": "laptop",
    "difficulty": "easy",
    "conversation": ["Busco laptop", "Para trabajo", "800 euros"],
    "expected_outcome": {"should_find_products": True, "min_products": 1}
}

result = evaluator.test_scenario(test_scenario)
print(result)
```

---

## 📦 Exportar/Importar Resultados

### Exportar a CSV
```python
import json
import csv

# Cargar JSON
with open('evaluation/results/orchestrator_20250111.json') as f:
    data = json.load(f)

# Exportar métricas a CSV
with open('metrics.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Escenario', 'Éxito', 'Tiempo', 'Productos'])
    
    for result in data['detailed_results']:
        writer.writerow([
            result['scenario_name'],
            result['overall_success'],
            result['execution_time'],
            result['metrics']['products_found']
        ])
```

### Generar Reporte desde Múltiples Archivos
```bash
python evaluation/report_generator.py \
  evaluation/results/questioner_20250111_120000.json \
  evaluation/results/rag_20250111_120000.json \
  evaluation/results/orchestrator_20250111_120000.json
```

---

## 🎯 Tips de Performance

### Reducir Tiempo de Evaluación
```python
# Opción 1: Evaluar menos escenarios
# Editar test_scenarios.json y comentar algunos

# Opción 2: Solo componentes rápidos
python evaluation/run_evaluation.py -c questioner

# Opción 3: Modificar K en RAG (menos resultados)
# En test_rag.py, cambiar k=10 a k=5
```

### Usar Gemini Flash (Más Rápido/Barato)
```python
# En llm_judge.py, cambiar modelo
LLM_JUDGE_CONFIG = {
    "model": "gemini-1.5-flash",  # En vez de gemini-1.5-pro
    "temperature": 0.1
}
```

---

## 📚 Recursos Adicionales

### Documentación
```bash
# Leer documentación completa
cat evaluation/README.md

# Guía rápida
cat evaluation/QUICKSTART.md

# Resumen de implementación
cat evaluation/IMPLEMENTATION_SUMMARY.md
```

### Ver Ejemplos
```bash
# Ver código de ejemplos
cat evaluation/examples.py

# Ejecutar todos los ejemplos
python evaluation/examples.py
```

---

## 💡 Recetas Útiles

### 1. Evaluación Rápida Pre-Commit
```bash
# Antes de hacer commit, ejecutar evaluación rápida
python evaluation/run_evaluation.py -c questioner
```

### 2. Benchmark de Rendimiento
```bash
# Medir tiempo de cada componente
time python evaluation/test_questioner.py
time python evaluation/test_rag.py
time python evaluation/test_orchestrator.py
```

### 3. Generar Reporte Comparativo
```python
# compare_reports.py
from evaluation.report_generator import ReportGenerator
import json

# Cargar dos versiones
old_data = json.load(open('results/old/orchestrator.json'))
new_data = json.load(open('results/new/orchestrator.json'))

# Generar reporte comparativo
generator = ReportGenerator()
# Implementar lógica de comparación...
```

---

## 🎓 Mejores Prácticas

1. **Ejecutar evaluación antes de cada release**
   ```bash
   python evaluation/run_evaluation.py
   ```

2. **Mantener historial de resultados**
   ```bash
   # No borrar archivos de results/, son tu historial
   ```

3. **Revisar tests fallidos individualmente**
   ```python
   # Ver detalles de tests fallidos en el JSON
   ```

4. **Ajustar umbrales según tu caso de uso**
   ```python
   # Editar config.py según necesidades
   ```

5. **Documentar cambios en escenarios**
   ```json
   // Agregar comentarios en test_scenarios.json
   ```

---

**¡Listo para evaluar! 🚀**

Para más información, consulta:
- `README.md` - Documentación completa
- `QUICKSTART.md` - Inicio rápido
- `examples.py` - Ejemplos prácticos

