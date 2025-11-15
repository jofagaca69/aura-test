"""
Tests end-to-end para el MultiAgentOrchestrator
"""
import json
import time
from typing import Dict, Any, List
from datetime import datetime

from src.orchestator import MultiAgentOrchestrator
from src.rag.vector_store import VectorStore
from evaluation.llm_judge import LLMJudge
from evaluation.config import THRESHOLDS


class OrchestratorEvaluator:
    """
    Evaluador end-to-end para el sistema completo
    """
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.orchestrator = MultiAgentOrchestrator(vector_store)
        self.llm_judge = LLMJudge()
        self.results = []
    
    def test_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta un escenario completo end-to-end
        
        Args:
            scenario: Escenario de prueba con conversación completa
            
        Returns:
            Resultados detallados de la evaluación
        """
        print(f"\n🧪 Testing E2E - Escenario: {scenario['name']}")
        print(f"   Categoría: {scenario['category']} | Dificultad: {scenario['difficulty']}")
        
        start_time = time.time()
        
        # Reiniciar orquestador
        self.orchestrator.reset()
        
        # Iniciar sesión
        initial_message = self.orchestrator.start_session()
        print(f"   🤖 Sistema: {initial_message[:60]}...")
        
        # Simular conversación completa
        conversation_log = [
            {"role": "assistant", "content": initial_message}
        ]
        
        responses = []
        for i, user_input in enumerate(scenario['conversation'], 1):
            print(f"   👤 Usuario {i}: {user_input[:60]}...")
            
            conversation_log.append({
                "role": "user",
                "content": user_input
            })
            
            # Procesar input
            result = self.orchestrator.process_user_input(user_input)
            responses.append(result)
            
            conversation_log.append({
                "role": "assistant", 
                "content": result.get('message', '')[:100] + "..."
            })
            
            print(f"   🤖 Estado: {result.get('status', 'unknown')}")
            
            # Si se completó, salir
            if result.get('status') == 'completed':
                break
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Obtener resultado final
        final_result = responses[-1] if responses else {}
        final_state = self.orchestrator.get_state()
        
        # Extraer datos del workflow
        workflow_data = self.orchestrator.workflow_data
        user_analysis = workflow_data.get('user_analysis', '')
        criteria = workflow_data.get('criteria', '')
        recommendations = workflow_data.get('recommendations', '')
        products_found = workflow_data.get('products_found', 0)
        
        # Evaluación 1: Completitud del flujo
        flow_success = final_state == 'completed'
        
        # Evaluación 2: Productos encontrados
        expected_outcome = scenario['expected_outcome']
        should_find = expected_outcome.get('should_find_products', True)
        min_products = expected_outcome.get('min_products', 1)
        products_ok = (
            (products_found >= min_products) if should_find 
            else (products_found == 0)
        )
        
        # Evaluación 3: Calidad de recomendaciones (LLM Judge)
        if recommendations and flow_success:
            recommendations_eval = self.llm_judge.evaluate_recommendations(
                user_analysis=user_analysis,
                search_criteria=str(criteria),
                recommendations=recommendations,
                products_found=products_found
            )
        else:
            recommendations_eval = {
                "success": False,
                "error": "No se generaron recomendaciones"
            }
        
        # Evaluación 4: Eficiencia temporal
        time_ok = execution_time <= THRESHOLDS['orchestrator']['avg_time_max']
        
        # Evaluación 5: Verificar palabras clave esperadas en recomendaciones
        relevance_keywords = expected_outcome.get('relevance_keywords', [])
        keyword_matches = 0
        if relevance_keywords and recommendations:
            rec_lower = recommendations.lower()
            for keyword in relevance_keywords:
                if keyword.lower() in rec_lower:
                    keyword_matches += 1
        
        keyword_relevance = (
            keyword_matches / len(relevance_keywords) 
            if relevance_keywords else 1.0
        )
        
        # Resultado consolidado
        test_result = {
            "scenario_id": scenario['id'],
            "scenario_name": scenario['name'],
            "scenario_difficulty": scenario['difficulty'],
            "timestamp": datetime.now().isoformat(),
            "execution_time": execution_time,
            "final_state": final_state,
            "conversation_log": conversation_log,
            "workflow_data": {
                "user_analysis": user_analysis,
                "criteria": criteria,
                "recommendations_preview": recommendations[:500] + "..." if recommendations else "",
                "products_found": products_found
            },
            "evaluations": {
                "flow_completed": flow_success,
                "products_found_ok": products_ok,
                "time_ok": time_ok,
                "keyword_relevance": keyword_relevance,
                "recommendations_quality": recommendations_eval
            },
            "metrics": {
                "execution_time": execution_time,
                "products_found": products_found,
                "conversation_turns": len(scenario['conversation']),
                "keyword_matches": keyword_matches,
                "keyword_total": len(relevance_keywords)
            },
            "overall_success": (
                flow_success and
                products_ok and
                time_ok and
                (keyword_relevance >= 0.5 if relevance_keywords else True)
            )
        }
        
        self.results.append(test_result)
        
        # Imprimir resumen
        print(f"\n   📊 Resultados:")
        print(f"      - Estado final: {final_state}")
        print(f"      - Productos encontrados: {products_found}")
        print(f"      - Tiempo ejecución: {execution_time:.2f}s")
        print(f"      - Relevancia keywords: {keyword_relevance:.2%}")
        
        if recommendations_eval.get('success'):
            eval_data = recommendations_eval['evaluation']
            print(f"      - Calidad recomendaciones: {eval_data.get('score_total', 'N/A'):.1f}/10")
            print(f"        · Relevancia: {eval_data.get('relevancia', 'N/A'):.1f}/10")
            print(f"        · Personalización: {eval_data.get('personalizacion', 'N/A'):.1f}/10")
            print(f"        · Explicación: {eval_data.get('explicacion', 'N/A'):.1f}/10")
        
        status = "✅ PASS" if test_result['overall_success'] else "❌ FAIL"
        print(f"   {status}")
        
        return test_result
    
    def run_all_tests(self, scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Ejecuta todos los escenarios end-to-end
        
        Args:
            scenarios: Lista de escenarios
            
        Returns:
            Resumen consolidado
        """
        print("\n" + "="*80)
        print("🧪 EVALUACIÓN END-TO-END DEL ORCHESTRATOR")
        print("="*80)
        
        self.results = []
        
        for scenario in scenarios:
            try:
                self.test_scenario(scenario)
            except Exception as e:
                print(f"   ❌ Error ejecutando escenario: {e}")
                import traceback
                traceback.print_exc()
                
                self.results.append({
                    "scenario_id": scenario['id'],
                    "scenario_name": scenario['name'],
                    "error": str(e),
                    "overall_success": False
                })
        
        # Calcular métricas agregadas
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.get('overall_success', False))
        
        # Métricas por dificultad
        by_difficulty = {}
        for result in self.results:
            diff = result.get('scenario_difficulty', 'unknown')
            if diff not in by_difficulty:
                by_difficulty[diff] = {"total": 0, "passed": 0}
            by_difficulty[diff]["total"] += 1
            if result.get('overall_success', False):
                by_difficulty[diff]["passed"] += 1
        
        # Métricas temporales
        execution_times = [
            r['execution_time'] 
            for r in self.results if 'execution_time' in r
        ]
        avg_time = sum(execution_times) / len(execution_times) if execution_times else 0
        max_time = max(execution_times) if execution_times else 0
        min_time = min(execution_times) if execution_times else 0
        
        # Métricas de productos
        products_counts = [
            r['metrics']['products_found'] 
            for r in self.results if 'metrics' in r and 'products_found' in r['metrics']
        ]
        avg_products = sum(products_counts) / len(products_counts) if products_counts else 0
        
        # Métricas de calidad LLM
        llm_scores = []
        for r in self.results:
            if 'evaluations' in r and 'recommendations_quality' in r['evaluations']:
                rec_eval = r['evaluations']['recommendations_quality']
                if rec_eval.get('success'):
                    score = rec_eval['evaluation'].get('score_total', 0)
                    llm_scores.append(score)
        
        avg_llm_score = sum(llm_scores) / len(llm_scores) if llm_scores else 0
        
        summary = {
            "component": "Orchestrator (End-to-End)",
            "timestamp": datetime.now().isoformat(),
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "success_rate": successful_tests / total_tests if total_tests > 0 else 0,
            "by_difficulty": by_difficulty,
            "metrics": {
                "execution_time": {
                    "avg": avg_time,
                    "max": max_time,
                    "min": min_time
                },
                "products_found": {
                    "avg": avg_products,
                    "counts": products_counts
                },
                "llm_judge_scores": {
                    "avg": avg_llm_score,
                    "all_scores": llm_scores,
                    "count": len(llm_scores)
                }
            },
            "thresholds": THRESHOLDS['orchestrator'],
            "all_thresholds_passed": {
                "success_rate": (successful_tests / total_tests) >= THRESHOLDS['orchestrator']['success_rate'] if total_tests > 0 else False,
                "avg_time": avg_time <= THRESHOLDS['orchestrator']['avg_time_max'],
                "avg_products": avg_products >= THRESHOLDS['orchestrator']['products_found_min']
            },
            "detailed_results": self.results
        }
        
        # Imprimir resumen detallado
        print("\n" + "="*80)
        print("📊 RESUMEN DE RESULTADOS - ORCHESTRATOR E2E")
        print("="*80)
        print(f"Tests ejecutados: {total_tests}")
        print(f"Tests exitosos: {successful_tests} ({successful_tests/total_tests*100:.1f}%)")
        print(f"Tests fallidos: {total_tests - successful_tests}")
        
        print(f"\n📈 Por dificultad:")
        for diff, stats in by_difficulty.items():
            rate = stats['passed'] / stats['total'] * 100 if stats['total'] > 0 else 0
            print(f"   - {diff}: {stats['passed']}/{stats['total']} ({rate:.1f}%)")
        
        print(f"\n⏱️  Tiempos de ejecución:")
        print(f"   - Promedio: {avg_time:.2f}s")
        print(f"   - Mínimo: {min_time:.2f}s")
        print(f"   - Máximo: {max_time:.2f}s")
        
        print(f"\n📦 Productos encontrados:")
        print(f"   - Promedio: {avg_products:.1f}")
        
        if llm_scores:
            print(f"\n🎯 Calidad (LLM Judge):")
            print(f"   - Score promedio: {avg_llm_score:.1f}/10")
            print(f"   - Evaluaciones completadas: {len(llm_scores)}/{total_tests}")
        
        print("\n✅ Umbrales:")
        for threshold_name, passed in summary['all_thresholds_passed'].items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {status} {threshold_name}")
        
        print("="*80 + "\n")
        
        return summary


def load_scenarios(filepath: str = "evaluation/datasets/test_scenarios.json") -> List[Dict[str, Any]]:
    """Carga escenarios de prueba"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['scenarios']


if __name__ == "__main__":
    # Cargar VectorStore
    print("🚀 Cargando VectorStore...")
    vector_store = VectorStore()
    vector_store.load_vectorstore()
    
    # Cargar escenarios
    scenarios = load_scenarios()
    
    # Crear evaluador
    evaluator = OrchestratorEvaluator(vector_store)
    
    # Ejecutar tests
    summary = evaluator.run_all_tests(scenarios)
    
    # Guardar resultados
    output_file = f"evaluation/results/orchestrator_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Resultados guardados en: {output_file}")

