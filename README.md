# Acelerador de Integraciones Open Source (B2B)
### Simulacion Laboral Abierta — NoCountry | Developer Tools / Consultoria Tech

Plataforma inteligente y catalogo interactivo de tecnologias open source curadas con **Asistente Consultor de Arquitectura mediante RAG (Retrieval-Augmented Generation)**, **Pipeline de Ingesta con GitHub API v3**, **Generador de Infraestructura como Codigo (docker-compose.yml)** y **Calculo Algoritmico de Metricas de Salud (Health Score)**.

Disenada para firmas de consultoria y equipos de ingenieria que gestionan multiples proyectos al ano, reduciendo de **15-20 horas a minutos** la investigacion y diseno de stacks tecnologicos, eliminando el vendor lock-in y maximizando el ahorro frente a herramientas SaaS propietarias.

---

## Caracteristicas Principales

### 1. Catalogo de Ingenieria (151+ Repositorios Curados)
- **Inventario Funcional de Alto Rendimiento**: 151 repositorios reales verificados y clasificados en 16 categorias tecnicas.
- **Categorias Funcionales**: Autenticacion & IAM, Base de Datos & BaaS, Busqueda & Vector, Inteligencia Artificial & LLMs, Analitica & BI, Pagos & Facturacion B2B, CMS Headless, Streaming & Colas, Automatizacion & Workflows, Monitoreo & Logs, Storage & Archivos, DevOps & Deploy, Seguridad & Secretos.
- **Buscador Full-Text FTS5 & Facetas**:
  - Busqueda instantanea impulsada por SQLite FTS5 sobre nombres, descripciones, tags y lenguajes.
  - Filtros tecnicos por lenguaje principal, licencia de software, nivel de salud y volumen de estrellas.
- **Modo de Visualizacion Dual**:
  - **Vista Cuadricula (Cards)**: Tarjetas con tags, auras de estado y micro-anillo de salud.
  - **Vista Tabla de Ingenieria (Data Matrix)**: Vista tabular densa para arquitectos de software con barras de salud horizontales y comparador rapido.
- **Micro-Gauges Circulares de Salud (SVG Rings)**:
  - Anillo de progreso circular que grafica el Health Score algoritmico (0 - 100%) con indicador esmeralda o cian.
- **Espectro de Color por Lenguaje**:
  - Indicadores visuales con el color oficial de cada ecosistema (TypeScript, Python, Go, Rust, JavaScript, C++, etc.).
- **Matriz de Comparacion Lado a Lado**:
  - Permite seleccionar hasta 4 herramientas y contrastarlas en una tabla comparativa con indicadores de adopcion, salud, alternativa SaaS, ahorro mensual y compatibilidad de stack.

---

### 2. Command Palette Global (Ctrl + K / Cmd + K)
- Buscador rapido y accesible en cualquier momento presionando `Ctrl + K`, `Cmd + K` o `/`.
- Navegacion completa por teclado (`Flecha Arriba`, `Flecha Abajo`, `Enter` para abrir la ficha tecnica, `Esc` para cerrar).
- Acceso directo a comandos del sistema, salto entre secciones y apertura instantanea de fichas tecnicas.

---

### 3. Asistente Consultor de Arquitectura (RAG Inteligente)
- **Input Contextual de Negocio**: Recibe requerimientos en lenguaje natural o mediante plantillas tecnicas preconfiguradas (`[LOGISTICS_TRACKING]`, `[HEALTH_TECH]`, `[ENTERPRISE_AI]`, `[IOT_STREAMING]`).
- **Analisis Semantico & Vectorial**: Descompone las necesidades del cliente en capas tecnicas y recupera los componentes optimos mediante indexacion vectorial TF-IDF con ponderacion de salud y reputacion.
- **Entregables de Consultoria**:
  - **Diagnostico y Resumen Ejecutivo**.
  - **Simulador de Escala de Equipo ROI**: Selector interactivo (10 devs, 50 devs, 250+ devs) que proyecta el ahorro anual en tiempo real.
  - **Estimador de Dimensionamiento de Servidores (Cloud Sizing)**: Calcula RAM minima (GB), vCPUs, almacenamiento NVMe, costo del VPS (Hetzner Cloud / AWS EC2) y el **Margen de Ahorro Neto**.
  - **Matriz de Cumplimiento & Seguridad (Zero Trust Ready)**: Indicadores de soberania GDPR, trazabilidad SOC 2, compatibilidad Air-Gapped y cifrado AES-256 / TLS 1.3.
  - **Generador de Despliegue en 1 Clic**:
    - **`docker-compose.yml` de produccion**: Ensamblado automaticamente con todos los servicios interconectados, redes privadas y volumenes persistentes.
    - **`.env.example` unificado**: Variables de entorno listas para desplegar.
    - **Blueprint en Markdown (.md)**: Documento completo para presentar a clientes y directores tecnicos.
  - **Topologia de Arquitectura Mermaid Interactiva**:
    - Controles de Zoom In (`+`), Zoom Out (`-`), Reset (`100%`) y Descarga de imagen en formato SVG vectorizado.

---

### 4. Conexion & Pipeline con GitHub REST API v3
El programa **si puede conectarse con todos los repositorios publicos de GitHub**. Cuenta con un motor de conexion preparado para produccion:

- **Conexion en Vivo de Cualquier Repositorio**:
  - Mediante el boton `+ Agregar Repo GitHub`, el usuario puede ingresar cualquier repositorio del mundo (`owner/repo`, ej: `directus/directus`, `posthog/posthog`).
  - El sistema consulta la API de GitHub en vivo, extrae metricas reales, ejecuta el calculo ponderado de salud y lo indexa inmediatamente en SQLite FTS5.
- **Manejo de Rate Limits de GitHub**:
  - Modo Anonimo: 60 peticiones/hora por IP.
  - Modo Autenticado: 5,000 peticiones/hora por token (configurable via variable de entorno `GITHUB_TOKEN`).
- **Rotacion de Tokens**:
  - Soporta multiples tokens separados por coma (`GITHUB_TOKENS=ghp_tok1,ghp_tok2`), alternando automaticamente entre ellos para multiplicar la cuota disponible.
- **Cache Inteligente con ETag (HTTP 304 Not Modified)**:
  - Almacena cabeceras ETag de cada repositorio. En sincronizaciones posteriores, si el repositorio no ha cambiado, GitHub responde con HTTP 304 y **no descuenta cuota del rate limit**.
- **Calculo Algoritmico de Health Score (0 - 100)**:
  - **Frescura de Commits (hasta 35 pts)**: Evaluacion de dias desde el ultimo push.
  - **Ratio de Resolucion de Issues (hasta 25 pts)**: Issues abiertos ponderados contra volumen de comunidad.
  - **Masa Critica (hasta 20 pts)**: Estrellas y forks.
  - **Licencia Permisiva (hasta 10 pts)**: MIT, Apache-2.0, BSD.
  - **Mantenimiento Activo (hasta 10 pts)**: Estado del mantenedor.

---

### 5. Suite de Consultoria White-Label & Blueprints de Clientes
- **Exportacion de Dossier Ejecutivo en PDF (White-Label)**:
  - Formato editorial corporativo disenado para entregar a directores tecnicos (CTOs) y clientes empresariales.
  - Incluye: membrete de confidencialidad, diagnostico ejecutivo, modelo financiero TCO, dimensionamiento de servidores VPS, matriz de cumplimiento Zero-Trust, topologia vectorial del sistema y firmas de conformidad cliente/consultor.
  - Optimizado para impresion en A4 o guardado en PDF de 1 clic mediante estandares `@media print`.
- **Persistencia de Blueprints de Clientes en SQLite**:
  - Permite guardar propuestas tecnicas asociadas al nombre del cliente y titulo del proyecto.
  - Cajon/Drawer de historial con listado cronologico de blueprints guardados.
  - Carga instantanea de cualquier blueprint previo directamente en el canvas interactivo.
- **Preparado para Despliegue Cloud en Produccion**:
  - `Dockerfile` optimizado y ligero (Python 3.12/3.14 slim).
  - `docker-compose.yml` para despliegue en 1 comando con volumen de persistencia `./data`.

---

### 6. Soporte Multi-Dispositivo & Progressive Web App (PWA)
- **Acceso Directo desde Moviles y Tablets (iOS & Android)**:
  - Deteccion automatica de la IP de red local (`get_local_ip()`).
  - Al iniciar el servidor, muestra la URL exacta para abrir desde cualquier celular o tablet conectado al mismo Wi-Fi sin instalar software adicional.
  - Boton `Acceso Movil` en el encabezado con visualizador de Codigo QR para escanear con la camara y boton de copiado rapido de URL.
- **Barra de Navegacion Inferior para Celulares (Mobile Bottom Tab Bar)**:
  - Diseno ergonomico para navegacion con el pulgar en pantallas tactiles (Catalogo, Consultor RAG, Pipeline y Busqueda).
  - Soporte de areas seguras para pantallas con notch o barra de gestos (`env(safe-area-inset-bottom)`).
- **Instalable como App (PWA)**:
  - Archivo `manifest.json` y metadatos `apple-mobile-web-app-capable`.
  - Icono SVG vectorial adaptable para pantalla de inicio en Android y iOS.
  - Optimizacion anti-zoom en inputs tactiles.

---

## Arquitectura de Archivos

```
b2b/
├── backend/
│   ├── app.py                 # Servidor HTTP RESTful con socket reuse, fallback y CRUD de blueprints
│   ├── database.py            # SQLite con FTS5, schema relacional y persistencia de blueprints
│   ├── health_score.py        # Algoritmo de puntuacion de salud tecnica (0-100)
│   ├── rag_engine.py          # Motor semantico RAG, generador de docker-compose, sizing y Mermaid
│   ├── seed_data.py           # Inventario curado de 151 repositorios open-source
│   └── pipeline/
│       ├── github_client.py   # Cliente GitHub API v3 con rate-limit, ETag y rotacion de tokens
│       └── sync_service.py    # Servicio de ingesta por lotes y auditoria
├── frontend/
│   ├── index.html             # Interfaz web SPA (Paleta Obsidian Cyber, Modales de Clientes, Print Area)
│   ├── css/
│   │   └── style.css          # Estilos Obsidian Cyber, health rings y reglas @media print White-Label
│   └── js/
│       ├── api.js             # Capa de comunicacion RESTful con endpoints de blueprints
│       ├── app.js             # Logica de catalogo, Command Palette (Ctrl+K), tabla de datos y modales
│       └── rag_chat.js        # Logica del consultor RAG, guardado de proyectos e impresion de dossier
├── data/
│   └── catalog.db             # Base de datos SQLite persistente con indices FTS5 y blueprints
├── tests/
│   ├── test_catalog.py        # Tests unitarios del catalogo, FTS5 y comparacion
│   ├── test_health_score.py   # Tests del algoritmo de salud
│   ├── test_rag_engine.py     # Tests del motor semantico RAG y sizing
│   ├── test_pipeline.py       # Tests del cliente GitHub y rotacion de tokens
│   └── test_blueprints.py     # Tests de persistencia y gestion de blueprints
├── Dockerfile                 # Imagen de contenedor ligera para despliegue en la nube
├── docker-compose.yml         # Orquestacion para autohospedaje con volumenes persistentes
├── .dockerignore              # Exclusion de temporales y caches para builds
├── run.sh                     # Script de ejecucion automatizada local
└── README.md                  # Documentacion tecnica del sistema
```

---

## Inicio Rapido

### Opcion A: Ejecucion Local (Directa)
```bash
cd /home/jugador/Descargas/b2b
./run.sh
```

El servidor detecta puertos libres e inicia el entorno en:
**`http://localhost:8080`**

### Opcion B: Despliegue con Docker
```bash
cd /home/jugador/Descargas/b2b
docker compose up -d
```
El contenedor compila la imagen, monta el volumen persistente en `./data` y expone el servicio en el puerto `8080`.

### Pruebas Unitarias
```bash
python3 -m unittest discover tests
```
Resultado: **16 tests ejecutados y aprobados (100% OK)**.

---

## Endpoints de la API REST

| Metodo | Endpoint | Descripcion |
|---|---|---|
| `GET` | `/api/repos` | Lista paginada con busqueda FTS5 y filtros |
| `GET` | `/api/repos/:id` | Ficha tecnica e idea de integracion de un repositorio |
| `GET` | `/api/repos/compare?ids=...` | Comparativa tecnica de multiples repositorios |
| `POST` | `/api/repos/add` | Analiza e ingesta un nuevo repositorio de GitHub en vivo |
| `GET` | `/api/categories` | Resumen de categorias con recuento |
| `GET` | `/api/filters` | Opciones de filtros dinamicos |
| `GET` | `/api/stats` | Estadisticas globales del catalogo y ahorros SaaS |
| `POST` | `/api/rag/recommend` | Motor RAG: Blueprint, docker-compose, sizing y Mermaid |
| `POST` | `/api/pipeline/sync` | Ejecuta lote de sincronizacion con GitHub API |
| `GET` | `/api/pipeline/logs` | Historial de auditoria de sincronizacion |
| `GET` | `/api/blueprints` | Lista de blueprints y proyectos de clientes guardados |
| `POST` | `/api/blueprints` | Guarda o actualiza un blueprint de consultoria de cliente |
| `GET` | `/api/blueprints/:id` | Detalle completo de un blueprint guardado |
| `POST` | `/api/blueprints/:id/delete` | Elimina un blueprint de la base de datos |
| `GET` | `/api/system/network` | IP local y URL de red para conexion desde moviles y tablets |
