"""
Orquestador del sistema multiagentes con recolección dinámica
"""
from typing import Dict, Any, Optional
from enum import Enum

from src.agents.dynamic_collector import DynamicInformationCollectorAgent
from src.agents.preference_analyzer import PreferenceAnalyzerAgent
from src.agents.recommender import RecommenderAgent
from src.rag.vector_store import VectorStore


class WorkflowState(Enum):
    """Estados del flujo de trabajo"""
    INIT = "init"
    COLLECTING_INFO = "collecting_info"
    ANALYZING_PREFERENCES = "analyzing_preferences"
    GENERATING_RECOMMENDATIONS = "generating_recommendations"
    COMPLETED = "completed"


class DynamicMultiAgentOrchestrator:
    """
    Orquestador que usa recolección dinámica de información
    """
    
    def __init__(self, vector_store: VectorStore):
        """
        Inicializa el orquestador con todos los agentes
        
        Args:
            vector_store: VectorStore con los productos indexados
        """
        self.vector_store = vector_store
        
        # Inicializar agentes
        self.collector = DynamicInformationCollectorAgent()
        self.analyzer = PreferenceAnalyzerAgent()
        self.recommender = RecommenderAgent(vector_store)
        
        # Estado del flujo
        self.state = WorkflowState.INIT
        self.workflow_data: Dict[str, Any] = {}
        self.current_question: Optional[str] = None
    
    def start_session(self) -> str:
        """
        Inicia una nueva sesión de recomendación
        
        Returns:
            Mensaje de bienvenida y primera pregunta
        """
        # Reiniciar agentes
        self.collector.reset()
        self.analyzer.clear_memory()
        self.recommender.clear_memory()
        
        # Reiniciar estado
        self.state = WorkflowState.COLLECTING_INFO
        self.workflow_data = {}
        
        # Generar primera pregunta dinámica
        self.current_question = self.collector.generate_next_question()
        
        greeting = f"""👋 ¡Hola! Soy AURA, tu asistente inteligente de recomendaciones.

Voy a hacerte algunas preguntas para entender exactamente lo que necesitas y así poder recomendarte los mejores productos.

{self.current_question}"""
        
        return greeting
    
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Procesa la entrada del usuario según el estado actual
        
        Args:
            user_input: Respuesta del usuario
            
        Returns:
            Respuesta del sistema con siguiente acción
        """
        if self.state == WorkflowState.COLLECTING_INFO:
            return self._handle_dynamic_collection(user_input)
        
        elif self.state == WorkflowState.COMPLETED:
            # Permitir preguntas adicionales sobre las recomendaciones
            return self._handle_followup_question(user_input)
        
        else:
            return {
                "message": "Estado inválido del sistema. Por favor, reinicia la sesión.",
                "status": "error"
            }
    
    def _handle_dynamic_collection(self, user_input: str) -> Dict[str, Any]:
        """
        Maneja la recolección dinámica de información
        
        Args:
            user_input: Respuesta del usuario
            
        Returns:
            Siguiente pregunta o inicio del análisis
        """
        # Generar siguiente pregunta basada en la respuesta
        next_question = self.collector.generate_next_question(user_input)
        
        # Verificar si tenemos suficiente información
        if next_question is None or self.collector.is_information_sufficient():
            print("\n✓ Información suficiente recopilada")
            return self._process_workflow()
        
        # Continuar con siguiente pregunta
        self.current_question = next_question
        
        return {
            "message": next_question,
            "status": "collecting",
            "progress": f"{self.collector.questions_asked}/{self.collector.max_questions}"
        }
    
    def _process_workflow(self) -> Dict[str, Any]:
        """
        Ejecuta el flujo completo de análisis y recomendación
        
        Returns:
            Recomendaciones finales
        """
        try:
            # Paso 1: Analizar conversación completa
            print("\n🔍 Analizando la conversación...")
            self.state = WorkflowState.ANALYZING_PREFERENCES
            
            collector_result = self.collector.process({})
            self.workflow_data['user_analysis'] = collector_result['analysis']
            self.workflow_data['conversation_history'] = collector_result['conversation_history']
            
            # Paso 2: Generar criterios de búsqueda
            print("📊 Generando criterios de búsqueda optimizados...")
            
            analyzer_result = self.analyzer.process({
                'user_analysis': self.workflow_data['user_analysis']
            })
            self.workflow_data['criteria'] = analyzer_result['criteria']
            self.workflow_data['search_query'] = analyzer_result['search_query']
            
            # Paso 3: Generar recomendaciones
            print("🎯 Buscando los mejores productos para ti...")
            self.state = WorkflowState.GENERATING_RECOMMENDATIONS
            
            recommender_result = self.recommender.process({
                'search_query': self.workflow_data['search_query'],
                'criteria': self.workflow_data['criteria'],
                'user_analysis': self.workflow_data['user_analysis']
            })
            
            self.workflow_data['recommendations'] = recommender_result['recommendations']
            self.workflow_data['products_found'] = recommender_result['products_found']
            
            # Completado
            self.state = WorkflowState.COMPLETED
            
            return {
                "message": self._format_final_response(),
                "status": "completed",
                "recommendations": self.workflow_data['recommendations'],
                "products_found": self.workflow_data['products_found']
            }
            
        except Exception as e:
            return {
                "message": f"Error procesando la información: {str(e)}",
                "status": "error"
            }
    
    def _format_final_response(self) -> str:
        """
        Formatea la respuesta final con las recomendaciones
        
        Returns:
            Respuesta formateada
        """
        response = f"""
✨ ¡Perfecto! He analizado toda nuestra conversación y encontré {self.workflow_data['products_found']} productos relevantes.

📋 RECOMENDACIONES PERSONALIZADAS:

{self.workflow_data['recommendations']}

---

💬 ¿Tienes alguna pregunta sobre estas recomendaciones?
Puedo ayudarte con:
- Comparar productos específicos en detalle
- Explicar más sobre alguna característica
- Buscar alternativas
- Aclarar cualquier duda
"""
        return response
    
    def _handle_followup_question(self, user_input: str) -> Dict[str, Any]:
        """
        Maneja preguntas de seguimiento sobre las recomendaciones
        
        Args:
            user_input: Pregunta del usuario
            
        Returns:
            Respuesta a la pregunta
        """
        from langchain_core.prompts import ChatPromptTemplate
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres AURA, un asistente experto en productos.
            Ya has generado recomendaciones para el usuario después de una conversación detallada.
            Ahora responde sus preguntas adicionales basándote en:
            1. Las recomendaciones que ya hiciste
            2. El análisis del usuario
            3. Los productos disponibles
            4. La conversación que tuvieron
            
            Sé útil, específico, conversacional y amigable."""),
            ("user", """CONTEXTO:

Conversación previa:
{conversation_summary}

Análisis del usuario:
{user_analysis}

Recomendaciones previas:
{recommendations}

PREGUNTA DEL USUARIO:
{question}

Por favor, responde la pregunta de forma clara y útil:""")
        ])
        
        chain = prompt | self.recommender.llm
        
        # Crear resumen de conversación
        conversation_summary = "\n".join([
            f"{'AURA' if msg['role'] == 'assistant' else 'Usuario'}: {msg['content']}"
            for msg in self.workflow_data.get('conversation_history', [])[-4:]
        ])
        
        result = chain.invoke({
            "conversation_summary": conversation_summary,
            "user_analysis": self.workflow_data.get('user_analysis', ''),
            "recommendations": self.workflow_data.get('recommendations', ''),
            "question": user_input
        })
        
        return {
            "message": result.content,
            "status": "followup"
        }
    
    def get_state(self) -> str:
        """Obtiene el estado actual del flujo"""
        return self.state.value
    
    def reset(self):
        """Reinicia el orquestador"""
        self.collector.reset()
        self.analyzer.clear_memory()
        self.recommender.clear_memory()
        self.state = WorkflowState.INIT
        self.workflow_data = {}
        self.current_question = None

