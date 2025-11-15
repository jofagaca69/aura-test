"""
Ejemplos prácticos de uso del sistema de evaluación AURA
"""
import sys
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.vector_store import VectorStore
from evaluation.test_questioner import QuestionerEvaluator, load_scenarios
from evaluation.test_rag import RAGEvaluator
from evaluation.test_orchestrator import OrchestratorEvaluator
from evaluation.llm_judge import LLMJudge


# ============================================================================
# EJEMPLO 1: Evaluar un escenario específico del QuestionerAgent
# ============================================================================

def example_1_questioner_single_scenario():
    """
    Evalúa un solo escenario del QuestionerAgent
    Útil para debug o análisis detallado
    """
    print("\n" + "="*80)
    print("EJEMPLO 1: Test Individual - QuestionerAgent")
    print("="*80)
    
    # Cargar escenarios
    scenarios = load_scenarios()
    
    # Seleccionar uno específico (por ejemplo, el primero)
    scenario = scenarios[0]
    
    # Crear evaluador
    evaluator = QuestionerEvaluator()
    
    # Ejecutar test
    result = evaluator.test_scenario(scenario)
    
    # Analizar resultados
    print("\n📊 Análisis del resultado:")
    print(f"  Escenario: {result['scenario_name']}")
    print(f"  Éxito: {'✅' if result['overall_success'] else '❌'}")
    print(f"  Precisión extracción: {result['extraction_evaluation']['accuracy_percentage']:.1f}%")
    print(f"  Preguntas realizadas: {result['questions_asked']}")
    print(f"  Score información: {result['information_score']:.1f}%")
    
    # Ver preguntas generadas
    print("\n❓ Preguntas generadas:")
    for i, q in enumerate(result['questions_list'], 1):
        print(f"  {i}. {q}")
    
    return result


# ============================================================================
# EJEMPLO 2: Evaluar búsqueda RAG con consulta custom
# ============================================================================

def example_2_rag_custom_query():
    """
    Prueba el sistema RAG con una consulta personalizada
    Útil para verificar recuperación de documentos
    """
    print("\n" + "="*80)
    print("EJEMPLO 2: Búsqueda RAG Custom")
    print("="*80)
    
    # Cargar VectorStore
    print("🚀 Cargando VectorStore...")
    vector_store = VectorStore()
    vector_store.load_vectorstore()
    
    # Crear evaluador
    evaluator = RAGEvaluator(vector_store)
    
    # Definir consultas de prueba
    test_queries = [
        {
            "query": "laptop para programación con 16GB RAM",
            "expected_keywords": ["laptop", "programación", "RAM", "16GB"]
        },
        {
            "query": "teléfono económico con buena batería",
            "expected_keywords": ["teléfono", "económico", "batería"]
        },
        {
            "query": "auriculares con cancelación de ruido",
            "expected_keywords": ["auriculares", "cancelación", "ruido"]
        }
    ]
    
    # Ejecutar búsquedas
    for test in test_queries:
        result = evaluator.test_retrieval(
            query=test["query"],
            expected_keywords=test["expected_keywords"],
            k=5
        )
        
        print(f"\n📊 Resultados para: '{test['query']}'")
        print(f"  Documentos encontrados: {result['num_results']}")
        print(f"  Tiempo: {result['search_time']:.3f}s")
        print(f"  Relevancia: {result['relevance_score']:.2%}")
        
        if result['results_preview']:
            print(f"\n  📄 Preview del primer resultado:")
            print(f"  {result['results_preview'][0]['content'][:150]}...")


# ============================================================================
# EJEMPLO 3: Evaluar flujo end-to-end con escenario custom
# ============================================================================

def example_3_e2e_custom_scenario():
    """
    Ejecuta un test end-to-end con un escenario personalizado
    Útil para probar casos de uso específicos
    """
    print("\n" + "="*80)
    print("EJEMPLO 3: Test E2E con Escenario Custom")
    print("="*80)
    
    # Cargar VectorStore
    print("🚀 Cargando VectorStore...")
    vector_store = VectorStore()
    vector_store.load_vectorstore()
    
    # Crear evaluador
    evaluator = OrchestratorEvaluator(vector_store)
    
    # Definir escenario custom
    custom_scenario = {
        "id": "custom_example",
        "name": "Test: Usuario busca laptop para diseño gráfico",
        "category": "laptop",
        "difficulty": "medium",
        "conversation": [
            "Necesito una laptop nueva",
            "La uso principalmente para diseño gráfico con Photoshop e Illustrator",
            "Mi presupuesto es de unos 1500 euros",
            "Necesito buena pantalla y al menos 16GB de RAM",
            "Prefiero marcas confiables como Apple o Dell"
        ],
        "expected_extraction": {
            "categoria_producto": "laptop",
            "presupuesto_max": 1500.0,
            "uso_principal": "diseño gráfico",
            "caracteristicas_clave": ["buena pantalla", "16GB RAM"],
            "preferencias_marca": ["Apple", "Dell"]
        },
        "expected_outcome": {
            "should_find_products": True,
            "min_products": 1,
            "max_questions": 5,
            "relevance_keywords": ["diseño", "gráfico", "pantalla", "RAM"]
        }
    }
    
    # Ejecutar test
    result = evaluator.test_scenario(custom_scenario)
    
    # Analizar resultados
    print("\n📊 Análisis del resultado:")
    print(f"  Estado final: {result['final_state']}")
    print(f"  Productos encontrados: {result['workflow_data']['products_found']}")
    print(f"  Tiempo ejecución: {result['execution_time']:.2f}s")
    print(f"  Éxito: {'✅' if result['overall_success'] else '❌'}")
    
    # Ver recomendaciones generadas
    if result['workflow_data']['recommendations_preview']:
        print("\n🎯 Preview de recomendaciones:")
        print(result['workflow_data']['recommendations_preview'])
    
    # Ver calidad según LLM Judge
    if result['evaluations']['recommendations_quality'].get('success'):
        eval_data = result['evaluations']['recommendations_quality']['evaluation']
        print("\n⭐ Evaluación de calidad (LLM Judge):")
        print(f"  Relevancia: {eval_data.get('relevancia', 'N/A'):.1f}/10")
        print(f"  Diversidad: {eval_data.get('diversidad', 'N/A'):.1f}/10")
        print(f"  Explicación: {eval_data.get('explicacion', 'N/A'):.1f}/10")
        print(f"  Personalización: {eval_data.get('personalizacion', 'N/A'):.1f}/10")
        print(f"  Completitud: {eval_data.get('completitud', 'N/A'):.1f}/10")
        print(f"  Score Total: {eval_data.get('score_total', 'N/A'):.1f}/10")
    
    return result


# ============================================================================
# EJEMPLO 4: Usar LLM Judge directamente
# ============================================================================

def example_4_llm_judge_direct():
    """
    Usa el LLM Judge directamente para evaluar recomendaciones
    Útil para evaluar outputs de forma independiente
    """
    print("\n" + "="*80)
    print("EJEMPLO 4: Uso Directo de LLM Judge")
    print("="*80)
    
    # Crear judge
    judge = LLMJudge()
    
    # Simular datos de entrada
    user_analysis = """
    El usuario busca una laptop para diseño gráfico.
    Presupuesto: 1500 euros
    Uso principal: Photoshop, Illustrator
    Características importantes: Buena pantalla, 16GB RAM
    Marcas preferidas: Apple, Dell
    """
    
    search_criteria = """
    Categoría: Laptops
    Precio: hasta 1500€
    RAM: mínimo 16GB
    Pantalla: alta calidad de color
    Uso: diseño gráfico profesional
    """
    
    recommendations = """
    He encontrado 3 opciones excelentes para ti:
    
    1. **MacBook Pro 14" M3** - 1499€
       - Pantalla Retina de alta calidad
       - 16GB RAM unificada
       - Excelente para diseño con Adobe Suite
       - Batería de larga duración
    
    2. **Dell XPS 15** - 1399€
       - Pantalla 4K OLED
       - 16GB RAM DDR5
       - NVIDIA RTX 3050
       - Gran rendimiento en diseño
    
    3. **HP Envy 16** - 1299€
       - Pantalla 2.5K IPS
       - 16GB RAM
       - RTX 4050
       - Buena relación calidad-precio
    """
    
    # Evaluar
    print("🤖 Evaluando recomendaciones con LLM Judge...")
    result = judge.evaluate_recommendations(
        user_analysis=user_analysis,
        search_criteria=search_criteria,
        recommendations=recommendations,
        products_found=3
    )
    
    if result['success']:
        eval_data = result['evaluation']
        
        print("\n⭐ Resultados de la evaluación:")
        print(f"  Relevancia: {eval_data['relevancia']}/10")
        print(f"  Diversidad: {eval_data['diversidad']}/10")
        print(f"  Explicación: {eval_data['explicacion']}/10")
        print(f"  Personalización: {eval_data['personalizacion']}/10")
        print(f"  Completitud: {eval_data['completitud']}/10")
        print(f"\n  📊 Score Total: {eval_data['score_total']}/10")
        print(f"  🏆 Veredicto: {eval_data['veredicto']}")
        
        print(f"\n💬 Comentarios:")
        print(f"  {eval_data['comentarios']}")
        
        if eval_data.get('areas_mejora'):
            print(f"\n🔧 Áreas de mejora:")
            print(f"  {eval_data['areas_mejora']}")
    else:
        print(f"❌ Error en evaluación: {result.get('error')}")
    
    return result


# ============================================================================
# EJEMPLO 5: Comparar rendimiento entre versiones
# ============================================================================

def example_5_compare_versions():
    """
    Compara resultados de evaluaciones de diferentes versiones
    Útil para tracking de mejoras
    """
    print("\n" + "="*80)
    print("EJEMPLO 5: Comparación de Versiones")
    print("="*80)
    
    import json
    from pathlib import Path
    
    # Buscar archivos de resultados
    results_dir = Path("evaluation/results")
    
    if not results_dir.exists():
        print("⚠️  No hay resultados previos para comparar")
        return
    
    # Buscar archivos orchestrator (los más completos)
    orchestrator_files = sorted(results_dir.glob("orchestrator_*.json"))
    
    if len(orchestrator_files) < 2:
        print(f"⚠️  Solo hay {len(orchestrator_files)} archivo(s). Se necesitan al menos 2 para comparar.")
        return
    
    # Comparar los 2 más recientes
    old_file = orchestrator_files[-2]
    new_file = orchestrator_files[-1]
    
    print(f"📊 Comparando:")
    print(f"  Anterior: {old_file.name}")
    print(f"  Actual: {new_file.name}")
    
    # Cargar datos
    with open(old_file, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    
    with open(new_file, 'r', encoding='utf-8') as f:
        new_data = json.load(f)
    
    # Comparar métricas clave
    print("\n📈 Comparación de métricas:")
    
    # Tasa de éxito
    old_rate = old_data['success_rate'] * 100
    new_rate = new_data['success_rate'] * 100
    diff_rate = new_rate - old_rate
    print(f"\n  Tasa de éxito:")
    print(f"    Anterior: {old_rate:.1f}%")
    print(f"    Actual: {new_rate:.1f}%")
    print(f"    Cambio: {diff_rate:+.1f}% {'📈' if diff_rate > 0 else '📉' if diff_rate < 0 else '➡️'}")
    
    # Tiempo promedio
    old_time = old_data['metrics']['execution_time']['avg']
    new_time = new_data['metrics']['execution_time']['avg']
    diff_time = new_time - old_time
    print(f"\n  Tiempo promedio:")
    print(f"    Anterior: {old_time:.2f}s")
    print(f"    Actual: {new_time:.2f}s")
    print(f"    Cambio: {diff_time:+.2f}s {'⚡ Más rápido' if diff_time < 0 else '🐌 Más lento' if diff_time > 0 else '➡️ Igual'}")
    
    # Calidad LLM
    old_llm = old_data['metrics']['llm_judge_scores']['avg']
    new_llm = new_data['metrics']['llm_judge_scores']['avg']
    diff_llm = new_llm - old_llm
    print(f"\n  Calidad LLM Judge:")
    print(f"    Anterior: {old_llm:.1f}/10")
    print(f"    Actual: {new_llm:.1f}/10")
    print(f"    Cambio: {diff_llm:+.1f} {'⭐ Mejor' if diff_llm > 0 else '⚠️ Peor' if diff_llm < 0 else '➡️ Igual'}")
    
    # Veredicto final
    print(f"\n🎯 Veredicto:")
    if diff_rate > 5 and diff_time < 0 and diff_llm > 0:
        print("  🌟 ¡Mejora significativa en todos los aspectos!")
    elif diff_rate > 0 or diff_llm > 0:
        print("  ✅ Mejoras detectadas")
    elif diff_rate < -5 or diff_llm < -1:
        print("  ⚠️  Regresión detectada - revisar cambios")
    else:
        print("  ➡️  Rendimiento similar")


# ============================================================================
# MAIN: Ejecutar ejemplos
# ============================================================================

def main():
    """Ejecuta todos los ejemplos"""
    print("\n" + "="*80)
    print("🧪 EJEMPLOS PRÁCTICOS - SISTEMA DE EVALUACIÓN AURA")
    print("="*80)
    
    ejemplos = [
        ("1", "QuestionerAgent - Escenario Individual", example_1_questioner_single_scenario),
        ("2", "RAG - Búsqueda Custom", example_2_rag_custom_query),
        ("3", "End-to-End - Escenario Custom", example_3_e2e_custom_scenario),
        ("4", "LLM Judge - Uso Directo", example_4_llm_judge_direct),
        ("5", "Comparación de Versiones", example_5_compare_versions)
    ]
    
    print("\nEjemplos disponibles:")
    for num, desc, _ in ejemplos:
        print(f"  {num}. {desc}")
    
    print("\n" + "="*80)
    
    # Opción: ejecutar ejemplo específico o todos
    import sys
    
    if len(sys.argv) > 1:
        ejemplo_num = sys.argv[1]
        for num, desc, func in ejemplos:
            if num == ejemplo_num:
                func()
                break
    else:
        # Ejecutar todos (comentar los que no quieras ejecutar)
        print("\n⚠️  Por defecto, ejecuta EJEMPLO 4 (más rápido)")
        print("Para ejecutar otro: python examples.py [1-5]\n")
        example_4_llm_judge_direct()


if __name__ == "__main__":
    main()

