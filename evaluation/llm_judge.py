"""
Evaluador LLM-as-Judge para evaluar la calidad de las recomendaciones
"""
import json
from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import config
from evaluation.config import LLM_JUDGE_CONFIG


class LLMJudge:
    """
    Evaluador basado en LLM que juzga la calidad de las recomendaciones
    Utiliza Gemini para evaluación consistente y objetiva
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=LLM_JUDGE_CONFIG["model"],
            temperature=LLM_JUDGE_CONFIG["temperature"],
            google_api_key=config.GOOGLE_API_KEY
        )
        
        # Prompt para evaluación de recomendaciones
        self.evaluation_prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres un evaluador experto de sistemas de recomendación de productos.
            Tu tarea es evaluar la calidad de las recomendaciones generadas por un asistente de IA.
            
            📊 CRITERIOS DE EVALUACIÓN (escala 0-10):
            
            1. **RELEVANCIA** (0-10):
               - ¿Los productos recomendados coinciden con las necesidades del usuario?
               - ¿Se respetan las restricciones de presupuesto?
               - ¿Las características solicitadas están presentes?
               
            2. **DIVERSIDAD** (0-10):
               - ¿Hay variedad apropiada en las opciones presentadas?
               - ¿Se ofrecen diferentes rangos de precio dentro del presupuesto?
               - ¿Se consideran diferentes marcas o alternativas?
               
            3. **EXPLICACIÓN** (0-10):
               - ¿Las justificaciones son claras y comprensibles?
               - ¿Se explica POR QUÉ cada producto es adecuado?
               - ¿Se mencionan pros y contras relevantes?
               
            4. **PERSONALIZACIÓN** (0-10):
               - ¿Las recomendaciones se adaptaron al contexto del usuario?
               - ¿Se consideró el uso específico mencionado?
               - ¿Se reflejan las preferencias expresadas?
               
            5. **COMPLETITUD** (0-10):
               - ¿Se abordaron todos los criterios mencionados por el usuario?
               - ¿Se proporcionó información suficiente para tomar una decisión?
               - ¿Se incluyeron detalles técnicos relevantes?
            
            📝 CONTEXTO DE LA EVALUACIÓN:
            
            **Análisis del usuario:**
            {user_analysis}
            
            **Criterios de búsqueda aplicados:**
            {search_criteria}
            
            **Recomendaciones generadas:**
            {recommendations}
            
            **Número de productos encontrados:**
            {products_found}
            
            🎯 INSTRUCCIONES:
            1. Evalúa cada criterio objetivamente
            2. Proporciona un score numérico (0-10) para cada uno
            3. Calcula el score total como promedio de los 5 criterios
            4. Proporciona comentarios específicos y constructivos
            5. Sugiere mejoras concretas si aplica
            
            ⚠️ SÉ ESTRICTO PERO JUSTO:
            - Un 10 es excepcional, raramente otorgado
            - Un 7-8 es bueno/muy bueno
            - Un 5-6 es aceptable pero mejorable
            - Menos de 5 indica problemas serios
            
            📋 RESPONDE EN FORMATO JSON VÁLIDO (sin markdown, sin comentarios):
            {{
                "relevancia": <número 0-10>,
                "diversidad": <número 0-10>,
                "explicacion": <número 0-10>,
                "personalizacion": <número 0-10>,
                "completitud": <número 0-10>,
                "score_total": <promedio de los 5 scores>,
                "comentarios": "<feedback específico sobre qué funcionó bien>",
                "areas_mejora": "<qué se podría mejorar>",
                "sugerencias": "<recomendaciones concretas para mejorar>",
                "veredicto": "<EXCELENTE|MUY_BUENO|BUENO|ACEPTABLE|DEFICIENTE>"
            }}"""),
            ("user", "Evalúa estas recomendaciones:")
        ])
        
        # Prompt para evaluar calidad de preguntas
        self.question_evaluation_prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres un evaluador experto de conversaciones de venta consultiva.
            Tu tarea es evaluar la calidad de las preguntas que hace un asistente de IA.
            
            📊 CRITERIOS DE EVALUACIÓN (escala 0-10):
            
            1. **CONTEXTUALIDAD** (0-10):
               - ¿Las preguntas se basan en respuestas previas?
               - ¿Hay conexión lógica entre preguntas?
               - ¿Se evita preguntar lo mismo dos veces?
               
            2. **RELEVANCIA** (0-10):
               - ¿Las preguntas son pertinentes para la búsqueda de productos?
               - ¿Ayudan a entender mejor las necesidades del usuario?
               - ¿Son específicas y enfocadas?
               
            3. **NATURALIDAD** (0-10):
               - ¿Suenan conversacionales y humanas?
               - ¿Evitan ser robóticas o formularias?
               - ¿Tienen el tono apropiado?
               
            4. **EFICIENCIA** (0-10):
               - ¿Se obtiene máxima información con mínimas preguntas?
               - ¿Son claras y fáciles de responder?
               - ¿No son redundantes?
               
            5. **COMPLETITUD** (0-10):
               - ¿Cubren todos los aspectos necesarios?
               - ¿Permiten recopilar información crítica?
               - ¿Siguen una secuencia lógica?
            
            📝 CONVERSACIÓN A EVALUAR:
            {conversation_history}
            
            📊 INFORMACIÓN EXTRAÍDA:
            {extracted_info}
            
            🎯 RESPONDE EN FORMATO JSON VÁLIDO:
            {{
                "contextualidad": <número 0-10>,
                "relevancia": <número 0-10>,
                "naturalidad": <número 0-10>,
                "eficiencia": <número 0-10>,
                "completitud": <número 0-10>,
                "score_total": <promedio>,
                "comentarios": "<análisis específico>",
                "mejores_preguntas": ["<ejemplos de preguntas bien hechas>"],
                "preguntas_mejorables": ["<ejemplos de preguntas que se podrían mejorar>"],
                "sugerencias": "<cómo mejorar>"
            }}"""),
            ("user", "Evalúa la calidad de estas preguntas:")
        ])
    
    def evaluate_recommendations(
        self, 
        user_analysis: str,
        search_criteria: str,
        recommendations: str,
        products_found: int
    ) -> Dict[str, Any]:
        """
        Evalúa la calidad de las recomendaciones usando Gemini
        
        Args:
            user_analysis: Análisis de las necesidades del usuario
            search_criteria: Criterios de búsqueda aplicados
            recommendations: Texto de recomendaciones generadas
            products_found: Número de productos encontrados
            
        Returns:
            Diccionario con scores y feedback
        """
        try:
            chain = self.evaluation_prompt | self.llm
            
            result = chain.invoke({
                "user_analysis": user_analysis or "No disponible",
                "search_criteria": search_criteria or "No disponible",
                "recommendations": recommendations or "No se generaron recomendaciones",
                "products_found": products_found
            })
            
            # Parsear JSON
            response_text = result.content.strip()
            
            # Limpiar markdown si está presente
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            evaluation = json.loads(response_text)
            
            return {
                "success": True,
                "evaluation": evaluation,
                "raw_response": result.content
            }
            
        except json.JSONDecodeError as e:
            print(f"⚠️ Error parseando JSON: {e}")
            print(f"Respuesta: {response_text[:500]}")
            return {
                "success": False,
                "error": "JSON parsing error",
                "raw_response": response_text
            }
        except Exception as e:
            print(f"⚠️ Error evaluando recomendaciones: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def evaluate_questions(
        self,
        conversation_history: str,
        extracted_info: str
    ) -> Dict[str, Any]:
        """
        Evalúa la calidad de las preguntas generadas por el QuestionerAgent
        
        Args:
            conversation_history: Historial completo de preguntas y respuestas
            extracted_info: Información extraída de las respuestas
            
        Returns:
            Diccionario con scores y feedback
        """
        try:
            chain = self.question_evaluation_prompt | self.llm
            
            result = chain.invoke({
                "conversation_history": conversation_history or "No hay conversación",
                "extracted_info": extracted_info or "No se extrajo información"
            })
            
            # Parsear JSON
            response_text = result.content.strip()
            
            # Limpiar markdown
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            evaluation = json.loads(response_text)
            
            return {
                "success": True,
                "evaluation": evaluation,
                "raw_response": result.content
            }
            
        except json.JSONDecodeError as e:
            print(f"⚠️ Error parseando JSON: {e}")
            return {
                "success": False,
                "error": "JSON parsing error",
                "raw_response": response_text
            }
        except Exception as e:
            print(f"⚠️ Error evaluando preguntas: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def evaluate_information_extraction(
        self,
        conversation: list,
        extracted_info: Dict[str, Any],
        expected_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evalúa la precisión de la extracción de información
        
        Args:
            conversation: Lista de intercambios [pregunta, respuesta]
            extracted_info: Información extraída por el sistema
            expected_info: Información esperada (ground truth)
            
        Returns:
            Métricas de precisión
        """
        scores = {}
        total_score = 0
        fields_evaluated = 0
        
        # Evaluar cada campo
        for field, expected_value in expected_info.items():
            extracted_value = extracted_info.get(field)
            
            if expected_value is None:
                # Si no se esperaba valor, verificar que no se extrajo nada incorrecto
                scores[field] = 1.0 if extracted_value is None or extracted_value == [] else 0.5
            elif isinstance(expected_value, list):
                # Para listas, calcular overlap
                if not expected_value:  # Lista vacía esperada
                    scores[field] = 1.0 if not extracted_value else 0.5
                else:
                    extracted_set = set(str(v).lower() for v in (extracted_value or []))
                    expected_set = set(str(v).lower() for v in expected_value)
                    
                    if not expected_set:
                        scores[field] = 1.0
                    else:
                        # Jaccard similarity
                        intersection = len(extracted_set & expected_set)
                        union = len(extracted_set | expected_set)
                        scores[field] = intersection / union if union > 0 else 0.0
            elif isinstance(expected_value, (int, float)):
                # Para números, verificar si está dentro del rango razonable
                if extracted_value is None:
                    scores[field] = 0.0
                else:
                    diff = abs(extracted_value - expected_value)
                    # Tolerancia del 10%
                    tolerance = expected_value * 0.1
                    scores[field] = 1.0 if diff <= tolerance else max(0, 1 - (diff / expected_value))
            else:
                # Para strings, verificar similitud semántica simple
                if extracted_value is None:
                    scores[field] = 0.0
                else:
                    extracted_lower = str(extracted_value).lower()
                    expected_lower = str(expected_value).lower()
                    
                    # Similitud básica: palabras en común
                    extracted_words = set(extracted_lower.split())
                    expected_words = set(expected_lower.split())
                    
                    if not expected_words:
                        scores[field] = 1.0
                    else:
                        overlap = len(extracted_words & expected_words)
                        scores[field] = overlap / len(expected_words)
            
            total_score += scores[field]
            fields_evaluated += 1
        
        # Calcular score promedio
        avg_score = total_score / fields_evaluated if fields_evaluated > 0 else 0.0
        
        return {
            "individual_scores": scores,
            "average_score": avg_score,
            "accuracy_percentage": avg_score * 100,
            "fields_evaluated": fields_evaluated,
            "perfect_matches": sum(1 for s in scores.values() if s >= 0.95),
            "partial_matches": sum(1 for s in scores.values() if 0.5 <= s < 0.95),
            "mismatches": sum(1 for s in scores.values() if s < 0.5)
        }

