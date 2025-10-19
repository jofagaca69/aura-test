"""
Sistema de almacenamiento vectorial con ChromaDB
"""
from typing import List, Optional
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

from src.config import config


class VectorStore:
    """Gestor del almacenamiento vectorial para RAG"""
    
    def __init__(self):
        # Usar embeddings locales para evitar límites de API
        print("🔧 Inicializando modelo de embeddings local...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        print("✓ Modelo de embeddings listo")
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        self.vectorstore: Optional[Chroma] = None
    
    def create_vectorstore(self, documents: List[Document]) -> Chroma:
        """
        Crea un vectorstore a partir de documentos
        
        Args:
            documents: Lista de documentos a indexar
            
        Returns:
            Vectorstore de Chroma
        """
        # Dividir documentos en chunks
        splits = self.text_splitter.split_documents(documents)
        
        print(f"📄 Documentos divididos en {len(splits)} chunks")
        
        # Crear directorio si no existe
        os.makedirs(config.CHROMA_DIR, exist_ok=True)
        
        # Crear vectorstore
        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=config.CHROMA_DIR
        )
        
        print(f"✓ Vectorstore creado con {len(splits)} embeddings")
        
        return self.vectorstore
    
    def load_vectorstore(self) -> Chroma:
        """
        Carga un vectorstore existente
        
        Returns:
            Vectorstore de Chroma
        """
        if not os.path.exists(config.CHROMA_DIR):
            raise ValueError(
                f"No existe vectorstore en {config.CHROMA_DIR}. "
                "Primero debes crear uno con create_vectorstore()"
            )
        
        self.vectorstore = Chroma(
            persist_directory=config.CHROMA_DIR,
            embedding_function=self.embeddings
        )
        
        print(f"✓ Vectorstore cargado desde {config.CHROMA_DIR}")
        
        return self.vectorstore
    
    def search(self, query: str, k: int = None) -> List[Document]:
        """
        Busca documentos similares a la consulta
        
        Args:
            query: Consulta de búsqueda
            k: Número de resultados a devolver
            
        Returns:
            Lista de documentos relevantes
        """
        if not self.vectorstore:
            raise ValueError("Vectorstore no inicializado")
        
        k = k or config.TOP_K_RESULTS
        
        results = self.vectorstore.similarity_search(query, k=k)
        
        return results
    
    def search_with_scores(self, query: str, k: int = None) -> List[tuple]:
        """
        Busca documentos con scores de similitud
        
        Args:
            query: Consulta de búsqueda
            k: Número de resultados a devolver
            
        Returns:
            Lista de tuplas (documento, score)
        """
        if not self.vectorstore:
            raise ValueError("Vectorstore no inicializado")
        
        k = k or config.TOP_K_RESULTS
        
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        
        return results
    
    def get_retriever(self, k: int = None):
        """
        Obtiene un retriever para usar con chains
        
        Args:
            k: Número de resultados a devolver
            
        Returns:
            Retriever de LangChain
        """
        if not self.vectorstore:
            raise ValueError("Vectorstore no inicializado")
        
        k = k or config.TOP_K_RESULTS
        
        return self.vectorstore.as_retriever(
            search_kwargs={"k": k}
        )

