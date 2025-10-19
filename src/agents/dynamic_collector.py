"""
Agente recolector dinámico que usa LLM para generar preguntas adaptativas
"""
from typing import Dict, Any, List, Optional
from langchain_core.prompts import ChatPromptTemplate

from src.agents.base_agent import BaseAgent


class DynamicInformationCollectorAgent(BaseAgent):
    """
    Agente que genera preguntas dinámicamente usando LLM
    según el contexto de la conversación
    """
    
    def __init__(self):
        super().__init__(
            name="Recolector Dinámico de Información",
            role="Recopilar preferencias mediante conversación adaptativa"
        )
        
        self.conversation_history: List[Dict[str, str]] = []
        self.information_gathered: Dict[str, Any] = {
            'presupuesto': None,
            'categoria': None,
            'caracteristicas': [],
            'uso_principal': None,
            'preferencias_marca': None,
            'prioridades': [],
            'restricciones': [],
        }
        self.questions_asked = 0
        self.max_questions = 7  # Máximo de preguntas antes de proceder
    
    def is_information_sufficient(self) -> bool:
        """
        Evalúa si tenemos suficiente información para hacer recomendaciones
        
        Returns:
            True si la información es suficiente
        """
        # Verificar campos críticos
        critical_fields = ['categoria', 'presupuesto']
        has_critical = all(self.information_gathered.get(field) for field in critical_fields)
        
        # O si ya hicimos suficientes preguntas
        return has_critical or self.questions_asked >= self.max_questions
    
    def generate_next_question(self, user_response: Optional[str] = None) -> str:
        """
        Genera la siguiente pregunta basada en el contexto
        
        Args:
            user_response: Última respuesta del usuario (None para primera pregunta)
            
        Returns:
            Siguiente pregunta a realizar
        """
        if user_response:
            # Guardar en historial
            self.conversation_history.append({
                'role': 'user',
                'content': user_response
            })
            
            # Extraer información de la respuesta
            self._extract_information(user_response)
        
        # Generar siguiente pregunta con contexto
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres un asistente experto en ventas que ayuda a los clientes a encontrar productos.

Tu objetivo es hacer UNA pregunta estratégica a la vez para entender las necesidades del cliente.

INFORMACIÓN QUE NECESITAS RECOPILAR:
1. Presupuesto aproximado
2. Categoría de producto (laptop, smartphone, electrodoméstico, etc.)
3. Características importantes para el usuario
4. Uso principal del producto
5. Preferencias de marca (si las hay)
6. Prioridades (precio, calidad, marca, características específicas)
7. Restricciones o limitaciones

INFORMACIÓN YA RECOPILADA:
{information_gathered}

CONVERSACIÓN HASTA AHORA:
{conversation_history}

INSTRUCCIONES:
- Haz UNA pregunta clara y específica
- Si falta información crítica (presupuesto o categoría), pregunta por eso primero
- Adapta la pregunta según lo que ya sabes
- Si ya tienes información sobre algo, no preguntes de nuevo
- Si el usuario mencionó algo pero no fue claro, pide aclaración
- Sé conversacional y amigable
- Si ya tienes suficiente información, responde solo: "INFORMACIÓN_COMPLETA"

Genera la siguiente pregunta:"""),
            ("user", "Última respuesta del usuario: {user_response}\n\nGenera la siguiente pregunta:")
        ])
        
        chain = prompt | self.llm
        
        result = chain.invoke({
            "information_gathered": self._format_information_gathered(),
            "conversation_history": self._format_conversation_history(),
            "user_response": user_response or "Primera interacción"
        })
        
        question = result.content.strip()
        
        # Verificar si el LLM indica que tiene suficiente información
        if "INFORMACIÓN_COMPLETA" in question or "INFORMACION_COMPLETA" in question:
            return None
        
        self.questions_asked += 1
        
        # Guardar pregunta en historial
        self.conversation_history.append({
            'role': 'assistant',
            'content': question
        })
        
        return question
    
    def _extract_information(self, user_response: str):
        """
        Extrae información estructurada de la respuesta del usuario usando LLM
        
        Args:
            user_response: Respuesta del usuario
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Analiza la respuesta del usuario y extrae información relevante.

INFORMACIÓN ACTUAL:
{current_info}

RESPUESTA DEL USUARIO:
{user_response}

Extrae y actualiza la siguiente información (solo menciona lo que encuentres en la respuesta):
- Presupuesto: [cantidad en dólares o rango]
- Categoría: [tipo de producto]
- Características: [lista de características mencionadas]
- Uso principal: [para qué lo usará]
- Preferencias de marca: [marcas mencionadas]
- Prioridades: [qué es más importante para el usuario]
- Restricciones: [limitaciones mencionadas]

Responde en formato estructurado. Si no encuentras información para algún campo, omítelo."""),
            ("user", "{user_response}")
        ])
        
        chain = prompt | self.llm
        
        result = chain.invoke({
            "current_info": self._format_information_gathered(),
            "user_response": user_response
        })
        
        # Actualizar información (simplificado - en producción usarías un parser más robusto)
        self.update_memory("last_extraction", result.content)
    
    def _format_information_gathered(self) -> str:
        """Formatea la información recopilada para el prompt"""
        lines = []
        for key, value in self.information_gathered.items():
            if value:
                lines.append(f"- {key}: {value}")
            else:
                lines.append(f"- {key}: [NO RECOPILADO]")
        return "\n".join(lines) if lines else "Ninguna información recopilada aún"
    
    def _format_conversation_history(self) -> str:
        """Formatea el historial de conversación"""
        if not self.conversation_history:
            return "Sin conversación previa"
        
        formatted = []
        for msg in self.conversation_history[-6:]:  # Últimos 6 mensajes
            role = "AURA" if msg['role'] == 'assistant' else "Usuario"
            formatted.append(f"{role}: {msg['content']}")
        
        return "\n".join(formatted)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa toda la conversación y genera análisis final
        
        Args:
            input_data: Datos de entrada (opcional)
            
        Returns:
            Análisis estructurado de la información recopilada
        """
        # Crear análisis completo de la conversación
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres un experto analizando necesidades de clientes.

Analiza la siguiente conversación y genera un resumen estructurado y detallado de:
1. Presupuesto del usuario
2. Tipo de producto que busca
3. Características prioritarias
4. Uso principal
5. Preferencias de marca
6. Factores de decisión más importantes
7. Cualquier restricción o limitación

CONVERSACIÓN COMPLETA:
{conversation_history}

Genera un análisis detallado y estructurado que será usado para buscar productos relevantes."""),
            ("user", "Por favor, analiza la conversación y genera el resumen:")
        ])
        
        chain = prompt | self.llm
        
        result = chain.invoke({
            "conversation_history": self._format_conversation_history()
        })
        
        analysis = result.content
        
        # Guardar en memoria
        self.update_memory("conversation_history", self.conversation_history)
        self.update_memory("analysis", analysis)
        
        return {
            "agent": self.name,
            "conversation_history": self.conversation_history,
            "analysis": analysis,
            "questions_asked": self.questions_asked,
            "status": "completed"
        }
    
    def reset(self):
        """Reinicia el agente para una nueva sesión"""
        self.conversation_history = []
        self.information_gathered = {
            'presupuesto': None,
            'categoria': None,
            'caracteristicas': [],
            'uso_principal': None,
            'preferencias_marca': None,
            'prioridades': [],
            'restricciones': [],
        }
        self.questions_asked = 0
        self.clear_memory()

