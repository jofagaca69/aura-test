"""
Script de configuración inicial del sistema AURA
"""
import os
import sys

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.rag.document_loader import DocumentLoader
from src.rag.vector_store import VectorStore
from src.config import config


def setup():
    """Configura el sistema por primera vez"""
    print("=" * 60)
    print("🔧 Configuración Inicial de AURA")
    print("=" * 60)
    print()
    
    # Verificar configuración
    try:
        config.validate()
        print("✓ Configuración validada")
    except ValueError as e:
        print(f"❌ Error: {e}")
        return False
    
    # Crear directorios necesarios
    print("\n📁 Creando directorios...")
    os.makedirs(config.DATA_DIR, exist_ok=True)
    os.makedirs(config.PRODUCTS_DIR, exist_ok=True)
    print(f"✓ {config.DATA_DIR}")
    print(f"✓ {config.PRODUCTS_DIR}")
    
    # Cargar documentos
    print("\n📂 Cargando documentos de productos...")
    
    loader = DocumentLoader()
    
    try:
        documents = loader.load_documents(config.PRODUCTS_DIR)
        
        if not documents:
            print("⚠️ No se encontraron documentos")
            print("💡 Añade archivos de productos en data/products/")
            return False
        
        print(f"✓ {len(documents)} documentos cargados")
        
    except Exception as e:
        print(f"❌ Error cargando documentos: {e}")
        return False
    
    # Crear vectorstore
    print("\n🔮 Creando vectorstore...")
    
    vector_store = VectorStore()
    
    try:
        vector_store.create_vectorstore(documents)
        print("✓ Vectorstore creado exitosamente")
        
    except Exception as e:
        print(f"❌ Error creando vectorstore: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ ¡Configuración completada!")
    print("=" * 60)
    print("\nAhora puedes ejecutar: python main.py")
    print()
    
    return True


if __name__ == "__main__":
    success = setup()
    sys.exit(0 if success else 1)

