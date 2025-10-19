"""
AURA - Sistema Multiagentes de IA para Recomendaciones de Productos
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


def initialize_system():
    """
    Inicializa el sistema cargando documentos y creando el vectorstore
    """
    print("=" * 60)
    print("🚀 AURA - Sistema de Recomendaciones con IA")
    print("=" * 60)
    print()
    
    # Validar configuración
    try:
        config.validate()
    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
        print("\n💡 Crea un archivo .env basado en env.example")
        sys.exit(1)
    
    # Verificar si existe el vectorstore
    if os.path.exists(config.CHROMA_DIR):
        print("📦 Vectorstore existente encontrado")
        response = input("¿Deseas recargar los productos? (s/n): ").lower()
        
        if response != 's':
            print("✓ Usando vectorstore existente")
            vector_store = VectorStore()
            vector_store.load_vectorstore()
            return vector_store
    
    # Cargar documentos
    print("\n📂 Cargando documentos de productos...")
    
    if not os.path.exists(config.PRODUCTS_DIR):
        print(f"❌ No se encontró el directorio {config.PRODUCTS_DIR}")
        print("💡 Crea el directorio y añade archivos de productos")
        sys.exit(1)
    
    loader = DocumentLoader()
    
    try:
        documents = loader.load_documents(config.PRODUCTS_DIR)
        
        if not documents:
            print("❌ No se encontraron documentos válidos")
            sys.exit(1)
        
        print(f"✓ {len(documents)} documentos cargados")
        
    except Exception as e:
        print(f"❌ Error cargando documentos: {e}")
        sys.exit(1)
    
    # Crear vectorstore
    print("\n🔮 Creando embeddings y vectorstore...")
    
    vector_store = VectorStore()
    
    try:
        vector_store.create_vectorstore(documents)
        print("✓ Vectorstore creado exitosamente")
        
    except Exception as e:
        print(f"❌ Error creando vectorstore: {e}")
        sys.exit(1)
    
    return vector_store


def run_interactive_session(orchestrator: MultiAgentOrchestrator):
    """
    Ejecuta una sesión interactiva con el usuario
    
    Args:
        orchestrator: Orquestador del sistema multiagentes
    """
    print("\n" + "=" * 60)
    print("💬 Modo Interactivo")
    print("=" * 60)
    print("Escribe 'salir' para terminar, 'nuevo' para nueva sesión")
    print()
    
    # Iniciar sesión
    greeting = orchestrator.start_session()
    print(greeting)
    print()
    
    while True:
        # Obtener entrada del usuario
        user_input = input("Tú: ").strip()
        
        if not user_input:
            continue
        
        # Comandos especiales
        if user_input.lower() == 'salir':
            print("\n👋 ¡Hasta pronto!")
            break
        
        if user_input.lower() == 'nuevo':
            print("\n🔄 Iniciando nueva sesión...\n")
            greeting = orchestrator.start_session()
            print(greeting)
            print()
            continue
        
        # Procesar entrada
        try:
            response = orchestrator.process_user_input(user_input)
            
            print("\n" + "-" * 60)
            print("AURA:", response['message'])
            print("-" * 60)
            print()
            
            if response['status'] == 'error':
                print("⚠️ Ocurrió un error. Intenta de nuevo o escribe 'nuevo'")
                print()
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Escribe 'nuevo' para reiniciar o 'salir' para terminar")
            print()


def main():
    """Función principal"""
    try:
        # Inicializar sistema
        vector_store = initialize_system()
        
        # Crear orquestador
        orchestrator = MultiAgentOrchestrator(vector_store)
        
        # Ejecutar sesión interactiva
        run_interactive_session(orchestrator)
        
    except KeyboardInterrupt:
        print("\n\n👋 Sesión interrumpida. ¡Hasta pronto!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
