# 🚀 Guía Rápida de AURA

## Instalación en 3 Pasos

### 1️⃣ Instalar Dependencias

```bash
pip install -e .
```

### 2️⃣ Configurar API Key

Crea un archivo `.env`:

```bash
GOOGLE_API_KEY=tu_api_key_de_google
MODEL_NAME=gemini-1.5-flash
TEMPERATURE=0.7
```

**Obtén tu API Key gratis en**: https://makersuite.google.com/app/apikey

### 3️⃣ Ejecutar

```bash
python main.py
```

## 📝 Ejemplo de Uso

```
🚀 AURA - Sistema de Recomendaciones con IA

¿Cuál es tu presupuesto aproximado para esta compra?
Tú: 1000 dólares

¿Qué tipo de producto estás buscando?
Tú: Una laptop para programación

¿Qué características son más importantes para ti?
Tú: Buena RAM, procesador rápido, portátil

...

✨ ¡Análisis completado!

📋 RECOMENDACIONES PERSONALIZADAS:

1. Dell XPS 13 - $1,299.99
   ✓ Excelente para programación
   ✓ 16GB RAM, Intel i7
   ✓ Ultraportátil (1.2kg)
   ...
```

## 🎯 Comandos

- **`nuevo`**: Nueva sesión de recomendación
- **`salir`**: Cerrar el programa

## 📂 Añadir Tus Productos

Coloca tus archivos en `data/products/`:

- ✅ JSON
- ✅ CSV
- ✅ TXT
- ✅ PDF
- ✅ DOCX
- ✅ XLSX

El sistema los procesará automáticamente.

## 🔧 Scripts Útiles

### Configuración Inicial
```bash
python scripts/setup.py
```

### Probar Agentes
```bash
python scripts/test_agents.py
```

## ⚠️ Problemas Comunes

### "GOOGLE_API_KEY no configurada"
→ Crea el archivo `.env` con tu API Key

### "No se encontraron documentos"
→ Añade archivos en `data/products/`

### Error de embeddings
→ Verifica tu conexión a internet y API Key

## 📚 Documentación Completa

Ver `README.md` para información detallada.

## 💡 Características

- ✅ Sistema multiagentes inteligente
- ✅ RAG con ChromaDB
- ✅ Múltiples formatos de archivo
- ✅ Recomendaciones personalizadas
- ✅ Conversación natural
- ✅ Google Gemini

---

**¿Necesitas ayuda?** Abre un issue en el repositorio.

