# 🤖 AURA - Sistema Multiagentes de IA con RAG

**AURA** (Asistente Universal de Recomendaciones Avanzadas) es un sistema multiagentes inteligente que utiliza RAG (Retrieval-Augmented Generation) para procesar información de productos desde múltiples tipos de archivos y generar recomendaciones personalizadas basadas en las preferencias del usuario.

## 🌟 Características Principales

- **Sistema Multiagentes**: Arquitectura modular con agentes especializados
- **RAG Avanzado**: Procesamiento de documentos con ChromaDB y embeddings de Google
- **Múltiples Formatos**: Soporte para PDF, CSV, JSON, TXT, DOCX, XLSX
- **Recomendaciones Personalizadas**: Análisis profundo de preferencias del usuario
- **Google Gemini**: Integración con modelos de IA de última generación
- **Conversacional**: Interfaz interactiva natural

## 🏗️ Arquitectura del Sistema

### Agentes Especializados

1. **Agente Recolector de Información** (`InformationCollectorAgent`)
   - Realiza preguntas estratégicas al usuario
   - Recopila preferencias, presupuesto y necesidades
   - Estructura la información para análisis

2. **Agente Analizador de Preferencias** (`PreferenceAnalyzerAgent`)
   - Analiza en profundidad las respuestas del usuario
   - Genera criterios de búsqueda optimizados
   - Prioriza características según importancia

3. **Agente Recomendador** (`RecommenderAgent`)
   - Utiliza RAG para buscar productos relevantes
   - Genera recomendaciones personalizadas
   - Explica por qué cada producto es adecuado

### Orquestador

El `MultiAgentOrchestrator` coordina el flujo de trabajo entre agentes:
- Gestiona el estado de la conversación
- Coordina la comunicación entre agentes
- Maneja preguntas de seguimiento

### Sistema RAG

- **DocumentLoader**: Carga documentos de múltiples formatos
- **VectorStore**: Gestiona embeddings con ChromaDB
- **Búsqueda Semántica**: Encuentra productos relevantes por significado

## 📋 Requisitos

- Python 3.10 o superior
- API Key de Google (para Gemini y embeddings)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <tu-repositorio>
cd AURA
```

### 2. Instalar dependencias

```bash
pip install -e .
```

O manualmente:

```bash
pip install langchain langchain-google-genai langchain-community chromadb pypdf python-dotenv pandas openpyxl python-docx tiktoken
```

### 3. Configurar variables de entorno

Crea un archivo `.env` basado en `env.example`:

```bash
cp env.example .env
```

Edita `.env` y añade tu API Key de Google:

```env
GOOGLE_API_KEY=tu_api_key_aqui
MODEL_NAME=gemini-1.5-flash
TEMPERATURE=0.7
```

### 4. Obtener API Key de Google

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una nueva API Key
3. Cópiala en tu archivo `.env`

## 📂 Estructura del Proyecto

```
AURA/
├── main.py                      # Punto de entrada principal
├── pyproject.toml              # Configuración del proyecto
├── env.example                 # Ejemplo de variables de entorno
├── README.md                   # Este archivo
│
├── src/
│   ├── config.py              # Configuración centralizada
│   ├── orchestrator.py        # Orquestador multiagentes
│   │
│   ├── agents/                # Agentes especializados
│   │   ├── base_agent.py
│   │   ├── information_collector.py
│   │   ├── preference_analyzer.py
│   │   └── recommender.py
│   │
│   └── rag/                   # Sistema RAG
│       ├── document_loader.py
│       └── vector_store.py
│
└── data/
    ├── products/              # Archivos de productos
    │   ├── productos_tecnologia.json
    │   ├── productos_hogar.csv
    │   └── productos_deportes.txt
    │
    └── chroma_db/            # Base de datos vectorial (generada)
```

## 💻 Uso

### Modo Interactivo

Ejecuta el sistema:

```bash
python main.py
```

El sistema:
1. Cargará los documentos de productos
2. Creará embeddings (primera vez)
3. Iniciará una conversación interactiva

### Ejemplo de Conversación

```
🚀 AURA - Sistema de Recomendaciones con IA
============================================================

📂 Cargando documentos de productos...
✓ productos_tecnologia.json cargado
✓ productos_hogar.csv cargado
✓ productos_deportes.txt cargado
✓ 30 documentos cargados

🔮 Creando embeddings y vectorstore...
📄 Documentos divididos en 125 chunks
✓ Vectorstore creado con 125 embeddings

💬 Modo Interactivo
============================================================

👋 ¡Hola! Soy AURA, tu asistente de recomendaciones.

¿Cuál es tu presupuesto aproximado para esta compra?

Tú: Tengo alrededor de 1000 dólares

¿Qué tipo de producto estás buscando? (categoría)

Tú: Una laptop para programación

¿Qué características son más importantes para ti?

Tú: Necesito buena RAM, procesador rápido y que sea portátil

...
```

### Comandos Especiales

- `nuevo`: Inicia una nueva sesión de recomendación
- `salir`: Termina el programa

## 📝 Añadir Productos

### 1. Formato JSON

```json
[
  {
    "id": "PROD001",
    "nombre": "Producto Ejemplo",
    "categoria": "Categoría",
    "precio": 99.99,
    "marca": "Marca",
    "descripcion": "Descripción detallada...",
    "caracteristicas": ["Feature 1", "Feature 2"],
    "uso_recomendado": "Para quién es ideal",
    "stock": 10
  }
]
```

### 2. Formato CSV

```csv
id,nombre,categoria,precio,marca,descripcion,caracteristicas,uso_recomendado,stock
PROD001,Producto,Categoría,99.99,Marca,Descripción,Feature1|Feature2,Uso ideal,10
```

### 3. Formato TXT

```text
ID: PROD001
Nombre: Producto Ejemplo
Categoría: Categoría
Precio: $99.99
Marca: Marca

Descripción:
Descripción detallada del producto...

Características:
- Feature 1
- Feature 2

Uso Recomendado: Para quién es ideal
Stock: 10 unidades
```

### 4. Otros Formatos

También soporta:
- **PDF**: Catálogos de productos
- **DOCX**: Documentos de Word
- **XLSX**: Hojas de cálculo Excel

## 🔧 Configuración Avanzada

### Variables de Entorno

```env
# API Keys
GOOGLE_API_KEY=tu_api_key

# Modelo de IA
MODEL_NAME=gemini-1.5-flash    # o gemini-1.5-pro para mejor calidad
TEMPERATURE=0.7                 # 0.0 = más determinista, 1.0 = más creativo

# Configuración RAG
CHUNK_SIZE=1000                 # Tamaño de chunks de texto
CHUNK_OVERLAP=200               # Superposición entre chunks
TOP_K_RESULTS=5                 # Número de resultados en búsqueda
```

### Personalizar Preguntas

Edita `src/agents/information_collector.py`:

```python
self.questions = [
    "Tu pregunta personalizada 1",
    "Tu pregunta personalizada 2",
    # ...
]
```

## 🎯 Casos de Uso

### 1. Tienda de Tecnología
- Recomendaciones de laptops, smartphones, tablets
- Basadas en uso (gaming, trabajo, estudio)
- Considerando presupuesto y preferencias

### 2. Tienda de Hogar
- Electrodomésticos según necesidades familiares
- Muebles según espacio y estilo
- Productos de domótica

### 3. Tienda Deportiva
- Equipamiento según deporte practicado
- Nivel del usuario (principiante, avanzado)
- Objetivos de entrenamiento

### 4. Cualquier Catálogo
- El sistema es agnóstico al tipo de producto
- Solo necesita información estructurada
- Se adapta automáticamente

## 🧠 Cómo Funciona

### Flujo de Trabajo

```
1. Usuario inicia sesión
   ↓
2. Agente Recolector hace preguntas
   ↓
3. Usuario responde (5 preguntas)
   ↓
4. Agente Analizador procesa respuestas
   ↓
5. Genera criterios de búsqueda optimizados
   ↓
6. Agente Recomendador busca en vectorstore (RAG)
   ↓
7. Encuentra productos relevantes
   ↓
8. Genera recomendaciones personalizadas
   ↓
9. Usuario puede hacer preguntas adicionales
```

### Tecnologías Clave

- **LangChain**: Framework para aplicaciones con LLMs
- **Google Gemini**: Modelo de lenguaje avanzado
- **ChromaDB**: Base de datos vectorial
- **Google Embeddings**: Representaciones vectoriales de texto
- **RAG**: Combina búsqueda + generación

## 🔍 Troubleshooting

### Error: "GOOGLE_API_KEY no está configurada"

**Solución**: Crea un archivo `.env` con tu API Key:
```bash
cp env.example .env
# Edita .env y añade tu API Key
```

### Error: "No se encontraron documentos válidos"

**Solución**: Verifica que:
1. Existe el directorio `data/products/`
2. Hay archivos con formatos soportados
3. Los archivos no están vacíos

### Error al crear embeddings

**Solución**: 
1. Verifica tu conexión a internet
2. Confirma que tu API Key es válida
3. Revisa que no has excedido el límite de la API

### Recomendaciones no relevantes

**Solución**:
1. Añade más información en los archivos de productos
2. Usa descripciones detalladas
3. Ajusta `TOP_K_RESULTS` en `.env`
4. Considera usar `gemini-1.5-pro` para mejor calidad

## 🚀 Mejoras Futuras

- [ ] Interfaz web con Streamlit/Gradio
- [ ] Soporte para imágenes de productos
- [ ] Sistema de feedback del usuario
- [ ] Historial de conversaciones
- [ ] Comparación visual de productos
- [ ] Integración con APIs de tiendas
- [ ] Soporte multiidioma
- [ ] Análisis de sentimientos en reviews

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.

---

**Hecho con ❤️ usando Google Gemini y LangChain**

