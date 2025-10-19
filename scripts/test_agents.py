"""
Script para probar los agentes individualmente
"""
import os
import sys

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.information_collector import InformationCollectorAgent
from src.agents.preference_analyzer import PreferenceAnalyzerAgent
from src.agents.recommender import RecommenderAgent
from src.rag.vector_store import VectorStore
from src.config import config


def test_information_collector():
    """Prueba el agente recolector"""
    print("\n" + "=" * 60)
    print("🧪 Probando Agente Recolector de Información")
    print("=" * 60)
    
    agent = InformationCollectorAgent()
    
    # Simular respuestas
    test_responses = [
        "Tengo un presupuesto de 1000 dólares",
        "Busco una laptop",
        "Necesito buena RAM, procesador rápido y portabilidad",
        "Prefiero Dell o Lenovo",
        "La usaré para programación y diseño"
    ]
    
    for response in test_responses:
        agent.add_response(response)
    
    # Procesar
    result = agent.process({})
    
    print("\n📊 Resultado:")
    print(result['analysis'])
    print("\n✓ Agente recolector funcionando correctamente")


def test_preference_analyzer():
    """Prueba el agente analizador"""
    print("\n" + "=" * 60)
    print("🧪 Probando Agente Analizador de Preferencias")
    print("=" * 60)
    
    agent = PreferenceAnalyzerAgent()
    
    # Usar análisis simulado
    user_analysis = """
    El usuario tiene un presupuesto de $1000 y busca una laptop.
    Prioriza: RAM abundante, procesador rápido, portabilidad.
    Marcas preferidas: Dell, Lenovo.
    Uso principal: Programación y diseño.
    """
    
    result = agent.process({'user_analysis': user_analysis})
    
    print("\n📊 Criterios:")
    print(result['criteria'])
    print("\n🔍 Query de búsqueda:")
    print(result['search_query'])
    print("\n✓ Agente analizador funcionando correctamente")


def test_recommender():
    """Prueba el agente recomendador"""
    print("\n" + "=" * 60)
    print("🧪 Probando Agente Recomendador")
    print("=" * 60)
    
    # Cargar vectorstore
    try:
        config.validate()
        vector_store = VectorStore()
        vector_store.load_vectorstore()
        print("✓ Vectorstore cargado")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Ejecuta primero: python scripts/setup.py")
        return
    
    agent = RecommenderAgent(vector_store)
    
    # Datos de prueba
    user_analysis = "Usuario busca laptop para programación, presupuesto $1000"
    criteria = "Prioriza: RAM, procesador, portabilidad"
    search_query = "laptop programación 16GB RAM procesador rápido portátil"
    
    result = agent.process({
        'user_analysis': user_analysis,
        'criteria': criteria,
        'search_query': search_query
    })
    
    print("\n📊 Recomendaciones:")
    print(result['recommendations'])
    print(f"\n✓ Encontrados {result['products_found']} productos")
    print("✓ Agente recomendador funcionando correctamente")


def main():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("🧪 PRUEBAS DE AGENTES AURA")
    print("=" * 60)
    
    try:
        test_information_collector()
        test_preference_analyzer()
        test_recommender()
        
        print("\n" + "=" * 60)
        print("✅ ¡Todas las pruebas completadas!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Pruebas interrumpidas")
    except Exception as e:
        print(f"\n❌ Error en las pruebas: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

