"""
Script de prueba del sistema dinámico de AURA
"""
import sys
import os

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from src.config import config
from src.rag.vector_store import VectorStore
from src.orchestrator_dynamic import DynamicMultiAgentOrchestrator


def test_dynamic_system():
    """Prueba el sistema dinámico"""
    print("=" * 60)
    print("🧪 PRUEBA DEL SISTEMA DINÁMICO")
    print("=" * 60)
    print()
    
    # Validar configuración
    try:
        config.validate()
        print("✓ Configuración validada")
    except ValueError as e:
        print(f"❌ Error: {e}")
        return False
    
    # Cargar vectorstore existente
    print("\n📦 Cargando vectorstore...")
    vector_store = VectorStore()
    
    try:
        vector_store.load_vectorstore()
        print("✓ Vectorstore cargado")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Ejecuta primero: python test_system.py")
        return False
    
    # Crear orquestador dinámico
    print("\n🤖 Inicializando sistema dinámico...")
    orchestrator = DynamicMultiAgentOrchestrator(vector_store)
    print("✓ Orquestador dinámico inicializado")
    
    # Iniciar sesión
    print("\n" + "=" * 60)
    print("💬 SIMULACIÓN DE CONVERSACIÓN DINÁMICA")
    print("=" * 60)
    
    greeting = orchestrator.start_session()
    print(f"\n{greeting}\n")
    
    # Simular conversación más natural y variada
    respuestas = [
        "Estoy buscando algo para mi oficina en casa",
        "Mi presupuesto es flexible, pero preferiría no gastar más de 1500 dólares",
        "Principalmente voy a programar y hacer videollamadas. También uso Docker bastante",
        "Me gusta Dell, pero estoy abierto a otras opciones si son buenas",
        "Sí, viajo ocasionalmente, así que la portabilidad es importante"
    ]
    
    for i, respuesta in enumerate(respuestas, 1):
        print(f"👤 Usuario: {respuesta}\n")
        
        resultado = orchestrator.process_user_input(respuesta)
        
        if resultado['status'] == 'collecting':
            print(f"🤖 AURA: {resultado['message']}\n")
            print(f"   [Progreso: {resultado.get('progress', 'N/A')}]\n")
        
        elif resultado['status'] == 'completed':
            print("=" * 60)
            print("✨ RECOMENDACIONES GENERADAS (Sistema Dinámico)")
            print("=" * 60)
            print(resultado['message'])
            break
        
        elif resultado['status'] == 'error':
            print(f"❌ Error: {resultado['message']}")
            return False
    
    # Pregunta de seguimiento
    print("\n" + "=" * 60)
    print("💬 PREGUNTA DE SEGUIMIENTO")
    print("=" * 60)
    print("\n👤 Usuario: ¿Cuál es más ligera y tiene mejor batería?\n")
    
    resultado = orchestrator.process_user_input("¿Cuál es más ligera y tiene mejor batería?")
    print(f"🤖 AURA: {resultado['message']}")
    
    print("\n" + "=" * 60)
    print("✅ ¡PRUEBA DEL SISTEMA DINÁMICO COMPLETADA!")
    print("=" * 60)
    print("\n💡 Ventajas del sistema dinámico:")
    print("   ✓ Preguntas adaptadas al contexto")
    print("   ✓ Conversación más natural")
    print("   ✓ Detecta cuándo tiene suficiente información")
    print("   ✓ No hace preguntas redundantes")
    print("\n🚀 Ejecuta: python main_dynamic.py")
    
    return True


if __name__ == "__main__":
    try:
        success = test_dynamic_system()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Prueba interrumpida")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

