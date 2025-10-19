"""
Script de prueba automático del sistema AURA
"""
import sys
import os

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from src.config import config
from src.rag.document_loader import DocumentLoader
from src.rag.vector_store import VectorStore
from src.orchestrator import MultiAgentOrchestrator


def test_system():
    """Prueba el sistema completo"""
    print("=" * 60)
    print("🧪 PRUEBA DEL SISTEMA AURA")
    print("=" * 60)
    print()
    
    # Validar configuración
    try:
        config.validate()
        print("✓ Configuración validada")
    except ValueError as e:
        print(f"❌ Error: {e}")
        return False
    
    # Cargar documentos
    print("\n📂 Cargando documentos...")
    loader = DocumentLoader()
    documents = loader.load_documents(config.PRODUCTS_DIR)
    print(f"✓ {len(documents)} documentos cargados")
    
    # Crear vectorstore
    print("\n🔮 Creando vectorstore con embeddings locales...")
    vector_store = VectorStore()
    
    # Eliminar vectorstore anterior si existe
    if os.path.exists(config.CHROMA_DIR):
        import shutil
        shutil.rmtree(config.CHROMA_DIR)
        print("✓ Vectorstore anterior eliminado")
    
    vector_store.create_vectorstore(documents)
    print("✓ Vectorstore creado exitosamente")
    
    # Crear orquestador
    print("\n🤖 Inicializando sistema multiagentes...")
    orchestrator = MultiAgentOrchestrator(vector_store)
    print("✓ Orquestador inicializado")
    
    # Iniciar sesión de prueba
    print("\n" + "=" * 60)
    print("💬 SIMULACIÓN DE CONVERSACIÓN")
    print("=" * 60)
    
    greeting = orchestrator.start_session()
    print(f"\nAURA: {greeting}\n")
    
    # Simular respuestas del usuario
    respuestas = [
        "Tengo un presupuesto de 1200 dólares",
        "Busco una laptop para programación",
        "Necesito buena RAM, procesador rápido y que sea portátil",
        "Prefiero Dell o Lenovo",
        "La usaré principalmente para desarrollo de software con Docker y VMs"
    ]
    
    for i, respuesta in enumerate(respuestas, 1):
        print(f"Usuario: {respuesta}\n")
        resultado = orchestrator.process_user_input(respuesta)
        
        if resultado['status'] == 'collecting':
            print(f"AURA: {resultado['message']}\n")
        elif resultado['status'] == 'completed':
            print("=" * 60)
            print("✨ RECOMENDACIONES GENERADAS")
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
    print("\nUsuario: ¿Cuál tiene mejor batería?\n")
    
    resultado = orchestrator.process_user_input("¿Cuál tiene mejor batería?")
    print(f"AURA: {resultado['message']}")
    
    print("\n" + "=" * 60)
    print("✅ ¡PRUEBA COMPLETADA EXITOSAMENTE!")
    print("=" * 60)
    print("\n💡 El sistema está funcionando correctamente.")
    print("   Ahora puedes ejecutar: python main.py")
    
    return True


if __name__ == "__main__":
    try:
        success = test_system()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Prueba interrumpida")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

