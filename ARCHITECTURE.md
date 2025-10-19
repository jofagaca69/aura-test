# 🏗️ Arquitectura de AURA

## Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                         USUARIO                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      main.py                                 │
│  - Inicialización del sistema                               │
│  - Interfaz de usuario interactiva                          │
│  - Gestión de sesiones                                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              MultiAgentOrchestrator                         │
│  - Coordina el flujo entre agentes                         │
│  - Gestiona el estado de la conversación                   │
│  - Maneja preguntas de seguimiento                         │
└────────┬────────────┬────────────┬──────────────────────────┘
         │            │            │
         ▼            ▼            ▼
    ┌────────┐  ┌─────────┐  ┌──────────┐
    │Agente 1│  │Agente 2 │  │Agente 3  │
    └────────┘  └─────────┘  └──────────┘
```

## Flujo de Datos Detallado

```
1. INICIALIZACIÓN
   ┌──────────────────┐
   │ DocumentLoader   │
   │ - Lee archivos   │
   │ - Parsea datos   │
   └────────┬─────────┘
            │
            ▼
   ┌──────────────────┐
   │  VectorStore     │
   │ - Crea chunks    │
   │ - Genera embed.  │
   │ - Indexa en DB   │
   └──────────────────┘

2. RECOLECCIÓN DE INFORMACIÓN
   ┌─────────────────────────────┐
   │ InformationCollectorAgent   │
   │                             │
   │ Pregunta 1 → Respuesta 1    │
   │ Pregunta 2 → Respuesta 2    │
   │ Pregunta 3 → Respuesta 3    │
   │ Pregunta 4 → Respuesta 4    │
   │ Pregunta 5 → Respuesta 5    │
   │                             │
   │ ↓ Procesa con LLM           │
   │                             │
   │ Análisis Estructurado       │
   └─────────────┬───────────────┘
                 │
                 ▼

3. ANÁLISIS DE PREFERENCIAS
   ┌─────────────────────────────┐
   │ PreferenceAnalyzerAgent     │
   │                             │
   │ Input: Análisis usuario     │
   │                             │
   │ ↓ Procesa con LLM           │
   │                             │
   │ Output:                     │
   │ - Criterios prioritarios    │
   │ - Palabras clave            │
   │ - Filtros específicos       │
   │ - Query de búsqueda         │
   └─────────────┬───────────────┘
                 │
                 ▼

4. BÚSQUEDA RAG
   ┌─────────────────────────────┐
   │ RecommenderAgent            │
   │                             │
   │ Input: Query de búsqueda    │
   │                             │
   │ ↓ Búsqueda en VectorStore   │
   │                             │
   │ Productos Relevantes (Top K)│
   │                             │
   │ ↓ Genera con LLM            │
   │                             │
   │ Recomendaciones             │
   │ Personalizadas              │
   └─────────────┬───────────────┘
                 │
                 ▼
            USUARIO
```

## Componentes Principales

### 1. Sistema RAG

#### DocumentLoader
```python
Responsabilidades:
- Detectar tipo de archivo
- Cargar contenido
- Convertir a formato Document
- Manejar errores de lectura

Formatos soportados:
- PDF → PyPDFLoader
- CSV → Pandas + Custom
- JSON → Custom parser
- TXT → TextLoader
- DOCX → UnstructuredWordDocumentLoader
- XLSX → Pandas + Custom
```

#### VectorStore
```python
Responsabilidades:
- Dividir documentos en chunks
- Generar embeddings (Google)
- Almacenar en ChromaDB
- Búsqueda por similitud
- Gestionar persistencia

Tecnologías:
- ChromaDB (base vectorial)
- Google Embeddings (embedding-001)
- RecursiveCharacterTextSplitter
```

### 2. Agentes

#### InformationCollectorAgent
```python
Rol: Recolectar información del usuario

Proceso:
1. Presenta preguntas predefinidas
2. Almacena respuestas
3. Analiza con LLM
4. Estructura información

Output:
- Respuestas raw
- Análisis estructurado
```

#### PreferenceAnalyzerAgent
```python
Rol: Analizar preferencias profundamente

Proceso:
1. Recibe análisis del usuario
2. Identifica prioridades
3. Genera criterios de búsqueda
4. Crea query optimizada

Output:
- Criterios estructurados
- Query de búsqueda RAG
```

#### RecommenderAgent
```python
Rol: Generar recomendaciones

Proceso:
1. Ejecuta búsqueda RAG
2. Obtiene productos relevantes
3. Analiza con contexto del usuario
4. Genera recomendaciones personalizadas

Output:
- Lista de productos recomendados
- Justificación por producto
- Pros y contras
```

### 3. Orquestador

#### MultiAgentOrchestrator
```python
Responsabilidades:
- Gestionar estados del workflow
- Coordinar comunicación entre agentes
- Manejar flujo de datos
- Gestionar preguntas de seguimiento
- Mantener contexto de conversación

Estados:
- INIT
- COLLECTING_INFO
- ANALYZING_PREFERENCES
- GENERATING_RECOMMENDATIONS
- COMPLETED
```

## Tecnologías Utilizadas

### LangChain
- Framework principal
- Gestión de prompts
- Chains y agentes
- Integraciones

### Google Gemini
- Modelo de lenguaje: gemini-1.5-flash
- Embeddings: embedding-001
- API: langchain-google-genai

### ChromaDB
- Base de datos vectorial
- Almacenamiento persistente
- Búsqueda por similitud
- Eficiente y escalable

### Python Libraries
- pandas: Procesamiento CSV/Excel
- pypdf: Lectura de PDFs
- python-docx: Lectura de Word
- tiktoken: Tokenización

## Patrones de Diseño

### 1. Strategy Pattern
Cada agente implementa la interfaz `BaseAgent` con su propia estrategia de procesamiento.

### 2. Chain of Responsibility
El orquestador pasa datos entre agentes en secuencia.

### 3. Factory Pattern
`DocumentLoader` crea loaders específicos según el tipo de archivo.

### 4. Singleton Pattern
`Config` mantiene configuración global única.

## Flujo de Datos Completo

```
Usuario Input
    ↓
[Orquestador]
    ↓
[Agente 1: Recolector]
    ↓ (5 preguntas/respuestas)
Análisis Usuario
    ↓
[Agente 2: Analizador]
    ↓ (procesa con LLM)
Criterios + Query
    ↓
[Agente 3: Recomendador]
    ↓ (búsqueda RAG)
[VectorStore]
    ↓ (productos relevantes)
[Agente 3: Recomendador]
    ↓ (genera con LLM)
Recomendaciones
    ↓
[Orquestador]
    ↓
Usuario Output
```

## Escalabilidad

### Añadir Nuevos Agentes
1. Heredar de `BaseAgent`
2. Implementar método `process()`
3. Registrar en `MultiAgentOrchestrator`

### Añadir Nuevos Formatos
1. Añadir método en `DocumentLoader`
2. Registrar extensión en `supported_extensions`

### Optimizaciones Futuras
- Cache de embeddings
- Procesamiento paralelo de documentos
- Batch processing de queries
- Fine-tuning de embeddings
- Compresión de contexto

## Seguridad

- API Keys en variables de entorno
- No se almacenan datos sensibles
- Validación de configuración
- Manejo de errores robusto

## Monitoreo

Puntos de logging recomendados:
- Carga de documentos
- Creación de embeddings
- Consultas RAG
- Respuestas de agentes
- Errores y excepciones

