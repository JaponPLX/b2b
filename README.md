# 🚀 Acelerador de Integraciones Open Source (B2B)
### Simulación Laboral Abierta — NoCountry | Developer Tools / Consultoría Tech

Plataforma inteligente y catálogo interactivo de tecnologías open source curadas con **Asistente Consultor de Arquitectura mediante RAG (Retrieval-Augmented Generation)**, **Pipeline de Ingesta con GitHub API** y **Cálculo de Métricas de Salud (Health Score)**.

Diseñada para acelerar la toma de decisiones técnicas en firmas de consultoría y desarrollo de software que gestionan múltiples proyectos al año, reduciendo de **15-20 horas a minutos** la investigación y diseño de stacks tecnológicos, evitando reinventar la rueda y maximizando el ahorro frente a herramientas SaaS propietarias.

---

## 🌟 Características Principales

### 1. 📚 Catálogo Web Interactivo (150+ Repositorios Curados)
- **Inventario Funcional Extenso**: Supera con creces el requerimiento mínimo (151 repositorios reales cargados y verificados).
- **Categorización Funcional Completa**: Autenticación, Base de Datos & BaaS, Búsqueda & RAG, Inteligencia Artificial & LLMs, Analítica & Telemetría, Pagos & Facturación B2B, CMS Headless, Mensajería & Streaming, Automatización & Workflows, Monitoreo & Logs, Almacenamiento, DevOps & Deploy, Seguridad, etc.
- **Buscador Avanzado & Facetas**:
  - Búsqueda full-text en tiempo real impulsada por **SQLite FTS5** sobre nombres, descripciones, tags y lenguajes.
  - Filtros dinámicos por **Lenguaje** (TypeScript, Python, Go, Rust, Java, etc.), **Licencia** (MIT, Apache-2.0, BSD, AGPL), **Nivel de Mantenimiento** y **Estrellas Mínimas**.
- **Ficha Técnica & Ideas de Integración Estructuradas**:
  - Métricas de GitHub: Estrellas, forks, issues abiertos, última actualización, mantenedor activo.
  - Alternativa SaaS y estimación de ahorro financiero mensual.
  - Patrón de integración estructurado con tipo (Docker, SDK, Webhook, REST, CLI), compatibilidad de stacks, nivel de dificultad, explicación paso a paso y **snippets de código listos para copiar con 1 clic**.

### 2. 🧠 Asistente Consultor de Arquitectura (RAG Inteligente)
- **Input Contextual de Negocio**: Recibe requerimientos en lenguaje natural (ej: *"Estoy construyendo un e-commerce B2B de logística con tracking de flotas en tiempo real, autenticación multi-tenant y pagos recurrentes"*).
- **Análisis Semántico & Embeddings**: Descompone las necesidades del cliente en capacidades técnicas (Auth, DB, Search, Queues, Billing, Analytics, etc.) y realiza recuperación semántica mediante vectores TF-IDF con normalización coseno y ponderación de reputación.
- **Entregables del Asistente**:
  - **Diagnóstico y Resumen Ejecutivo**.
  - **Calculadora de Ahorro de Costos vs SaaS Propietario** (ej: Ahorros estimados de más de $1,400 USD/mes / $16,800 USD/año frente a combinaciones de Auth0 + Algolia + Datadog + Firebase).
  - **Mapa de Arquitectura Visual e Interactivo** renderizado con **Mermaid.js** en tiempo real.
  - **Stack Desglosado y Justificado por Capas**.
  - **Guía de Conexión e Interoperabilidad Paso a Paso** con fragmentos de código conectando los servicios entre sí.
  - **Exportación en 1 Clic**: Descarga el blueprint completo en formato Markdown (.md) para presentar a clientes y stakeholders.

### 3. 🔄 Pipeline de Ingesta & Sincronización GitHub
- **Respeto Estricto de Rate Limits**: Lee y monitorea los encabezados `x-ratelimit-remaining` y `x-ratelimit-reset`.
- **Caché Inteligente con ETag**: Emite peticiones condicionales con cabecera `If-None-Match` recibiendo respuestas `304 Not Modified` para no gastar cuota ni ancho de banda.
- **Rotación de Tokens & Backoff Exponencial con Jitter**: Soporta múltiples tokens en `GITHUB_TOKEN` y reintentos ante códigos 403 / 429.
- **Cálculo Algorítmico de Health Score (0 - 100)**:
  - **Frescura de Commits (hasta 35 pts)**: Ponderación basada en la fecha del último commit (< 14 días: 35 pts, < 45 días: 30 pts, etc.).
  - **Ratio de Issues Abiertos (hasta 25 pts)**: Pondera issues abiertos sobre el volumen de estrellas y forks para medir el nivel de resolución de la comunidad.
  - **Adopción y Masa Crítica (hasta 20 pts)**: Número de estrellas y forks.
  - **Licencia Empresarial Permisiva (hasta 10 pts)**: Puntuación máxima para MIT, Apache 2.0, BSD, ISC.
  - **Mantenedor Activo (hasta 10 pts)**: Verificación de soporte continuado.
- **Auditoría**: Tabla de historial de sincronizaciones con detalle de repositorios verificados, actualizados y cuota restante.

---

## 🏗️ Arquitectura del Sistema

```
b2b/
├── backend/
│   ├── app.py                 # Servidor HTTP RESTful de alto rendimiento
│   ├── database.py            # SQLite con FTS5, schema relacional y queries
│   ├── health_score.py        # Algoritmo de puntuación de salud (0-100)
│   ├── rag_engine.py          # Motor semántico RAG, similitud coseno y Mermaid
│   ├── seed_data.py           # Inventario curado de 151 repositorios open-source
│   └── pipeline/
│       ├── github_client.py   # Cliente GitHub API con rate-limit y caché
│       └── sync_service.py    # Servicio de ingesta por lotes y cron
├── frontend/
│   ├── index.html             # Interfaz web SPA moderna, limpia y responsiva
│   ├── css/
│   │   └── style.css          # Estilos complementarios y animaciones
│   └── js/
│       ├── api.js             # Capa de comunicación REST
│       ├── app.js             # Lógica de catálogo, filtros y modales
│       └── rag_chat.js        # Lógica del asistente consultor RAG
├── data/
│   └── catalog.db             # Base de datos SQLite persistente
├── tests/
│   ├── test_catalog.py        # Tests unitarios del catálogo y FTS5
│   ├── test_health_score.py   # Tests del cálculo de salud
│   ├── test_rag_engine.py     # Tests del motor de recomendación RAG
│   └── test_pipeline.py       # Tests del cliente GitHub y rotación de tokens
├── run.sh                     # Script de inicio en 1 comando
└── README.md                  # Documentación del proyecto
```

---

## ⚡ Inicio Rápido (Quickstart)

### Requisitos
- Python 3.10 o superior (compatible con Python 3.14).
- Sin dependencias externas obligatorias: utiliza la biblioteca estándar de Python (SQLite con FTS5, HTTP server, math, json).

### 1. Clonar y ejecutar en 1 comando:
```bash
./run.sh
```

El script inicializará y poblará la base de datos automáticamente e iniciará el servidor en:
👉 **`http://localhost:8080`**

### 2. Ejecutar la suite de pruebas unitarias:
```bash
python3 -m unittest discover tests
```
Resultado: **13 tests ejecutados y aprobados (100% OK)**.

### 3. Ejecutar sincronización manual del pipeline:
```bash
python3 -m backend.pipeline.sync_service --limit 10
```

---

## 🔌 API Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/repos` | Búsqueda full-text, filtros (categoría, lenguaje, licencia, stars) y paginación. |
| `GET` | `/api/repos/:id` | Ficha técnica completa de un repositorio con sus ideas de integración y snippets. |
| `GET` | `/api/categories` | Lista de categorías funcionales con conteo y promedio de salud. |
| `GET` | `/api/filters` | Opciones disponibles para los filtros de la interfaz. |
| `GET` | `/api/stats` | Estadísticas consolidadas (herramientas, health score promedio, ahorros SaaS). |
| `POST` | `/api/rag/recommend` | Motor RAG: envía `{ "prompt": "descripción de negocio" }` y recibe el blueprint. |
| `POST` | `/api/pipeline/sync` | Dispara un lote de sincronización con la API de GitHub. |
| `GET` | `/api/pipeline/logs` | Historial de auditoría de las últimas sincronizaciones. |

---

## 💡 Ejemplos de Consultas al Asistente RAG

1. **E-Commerce B2B de Logística**:
   - *Input*: `"Estoy construyendo un e-commerce B2B de logística con tracking de flotas en tiempo real, autenticación multi-tenant y pagos recurrentes"`
   - *Stack Recomendado*: Keycloak (Auth OIDC) + Supabase/PostgreSQL (DB & RLS) + Meilisearch (Catálogo rápido) + RabbitMQ/BullMQ (Streaming & Colas) + Medusa/Lago (Pagos B2B) + Grafana (Dashboards) + Coolify (Deploy).
   - *Ahorro Estimado*: **~$1,420 USD / mes** ($17,040 USD / año).

2. **Telemedicina & Salud**:
   - *Input*: `"SaaS de telemedicina con videollamadas, historias clínicas encriptadas y firma digital de consentimientos"`
   - *Stack Recomendado*: Supabase + Documenso (Firma digital de contratos) + Cal.com (Agendamiento de citas médicas) + Novu (Notificaciones a pacientes) + MinIO (Almacenamiento cifrado de historias médicas).

3. **Plataforma de Inteligencia Artificial Privada**:
   - *Input*: `"Plataforma corporativa de IA para análisis de contratos con modelos LLM locales y búsqueda vectorial"`
   - *Stack Recomendado*: Ollama (Inferencia privada de Llama 3) + Qdrant / ChromaDB (Base de datos vectorial) + LiteLLM (Proxy & Load balancing) + Langfuse (Observabilidad de LLMs) + Flowise (Orquestación visual).

---

## 🏆 Cumplimiento de Entregables Simulación NoCountry

- [x] **Catálogo Web Interactivo**: Interfaz responsiva con navegación por categorías funcionales, filtros avanzados (lenguaje, licencia, nivel de mantenimiento, stars) y buscador de texto instantáneo.
- [x] **Ficha Técnica e Ideas de Integración**: Cada herramienta cuenta con métricas de salud, alternativa SaaS, tipo de integración, snippets de código ejecutables y compatibilidad de stacks.
- [x] **Asistente Consultor de Arquitectura (RAG)**: Análisis de modelos de negocio en lenguaje natural, mapa de arquitectura interactivo (Mermaid), justificación técnica, matriz de ahorro de costos y guía paso a paso de interoperabilidad.
- [x] **Pipeline de Ingesta & Salud Continua**: Cliente GitHub resiliente a rate-limits con ETag/304, backoff exponencial, recálculo de Health Score (0-100) y logs de auditoría.
- [x] **Base de Datos Poblada**: Inventario funcional con **151 repositorios open-source populares** organizados por categorías funcionales con ideas de integración completas.
- [x] **Suite de Tests Automatizada**: Cobertura con pruebas unitarias para base de datos, motor RAG, pipeline y cálculo de salud.

