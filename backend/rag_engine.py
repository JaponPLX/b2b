"""
Motor RAG (Retrieval-Augmented Generation) y Consultor de Arquitectura B2B.
Combina análisis semántico de requerimientos, filtrado de metadatos,
cálculo de similitud coseno vectorial, generación de diagramas Mermaid
y matrices de ahorro de costos.
"""

import json
import math
import re
from typing import List, Dict, Any, Optional, Tuple
from backend.database import get_db_connection, DB_PATH


STOPWORDS = {
    "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como", "con", "contra",
    "cual", "cuando", "de", "del", "desde", "donde", "durante", "e", "el", "ella",
    "ellas", "ellos", "en", "entre", "era", "erais", "eramos", "eran", "eras", "eres",
    "es", "esa", "esas", "ese", "eso", "esos", "esta", "estaba", "estado", "estais",
    "estamos", "estan", "estar", "estas", "este", "esto", "estos", "estoy", "estuve",
    "fue", "fueron", "fui", "fuimos", "ha", "habeis", "habia", "habian", "habido",
    "habiendo", "habla", "han", "has", "hasta", "hay", "haya", "he", "hemos", "hube",
    "hubo", "la", "las", "le", "les", "lo", "los", "me", "mi", "mis", "mucho", "muchos",
    "muy", "mas", "mia", "mias", "mio", "mios", "nada", "ni", "no", "nos", "nosotras",
    "nosotros", "nuestra", "nuestras", "nuestro", "nuestros", "o", "os", "otra", "otras",
    "otro", "otros", "para", "pero", "poco", "por", "porque", "que", "quien", "quienes",
    "se", "sea", "sean", "seamos", "seais", "ser", "sera", "seran", "seria", "si",
    "sido", "siendo", "sin", "sobre", "sois", "solamente", "solo", "somos", "son", "soy",
    "su", "sus", "suya", "suyas", "suyo", "suyos", "tambien", "tanto", "te", "tendremos",
    "tendria", "tenga", "tengamos", "tengo", "tenia", "tenido", "ti", "tiene", "tienen",
    "toda", "todas", "todo", "todos", "tu", "tus", "tuve", "tuviste", "tuvo", "un", "una",
    "unas", "uno", "unos", "usa", "usar", "va", "vamos", "van", "vaya", "yo",
    "the", "and", "or", "to", "in", "on", "with", "for", "by", "of", "is", "are"
}


def tokenize(text: str) -> List[str]:
    if not text:
        return []
    words = re.findall(r"\b[a-zA-Z0-9_\-\.]{2,}\b", text.lower())
    return [w for w in words if w not in STOPWORDS]


class SemanticVectorIndex:

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.doc_vectors: Dict[str, Dict[str, float]] = {}
        self.doc_metadata: Dict[str, Dict[str, Any]] = {}
        self.idf: Dict[str, float] = {}
        self.all_terms: set = set()
        self.build_index()

    def build_index(self):
        conn = get_db_connection(self.db_path)
        cur = conn.cursor()
        cur.execute("""
        SELECT r.*, i.title as integ_title, i.explanation as integ_explanation, i.code_snippet
        FROM repositories r
        LEFT JOIN integrations i ON r.id = i.repo_id
        """)
        rows = cur.fetchall()
        conn.close()

        num_docs = len(rows)
        if num_docs == 0:
            return

        doc_frequencies: Dict[str, int] = {}
        raw_doc_tokens: Dict[str, List[str]] = {}

        for row in rows:
            r_dict = dict(row)
            repo_id = r_dict["id"]
            tags = " ".join(json.loads(r_dict["tags_json"] or "[]"))
            text_corpus = f"{r_dict['name']} {r_dict['category']} {r_dict['description']} {tags} {r_dict['language']} {r_dict.get('saas_alternative') or ''} {r_dict.get('integ_title') or ''} {r_dict.get('integ_explanation') or ''}"
            tokens = tokenize(text_corpus)
            raw_doc_tokens[repo_id] = tokens
            self.doc_metadata[repo_id] = r_dict

            unique_tokens = set(tokens)
            for t in unique_tokens:
                doc_frequencies[t] = doc_frequencies.get(t, 0) + 1
                self.all_terms.add(t)

        for term, df in doc_frequencies.items():
            self.idf[term] = math.log((num_docs + 1) / (df + 1)) + 1.0

        for repo_id, tokens in raw_doc_tokens.items():
            if not tokens:
                continue
            tf: Dict[str, float] = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1.0

            vec: Dict[str, float] = {}
            for t, count in tf.items():
                vec[t] = (1.0 + math.log(count)) * self.idf.get(t, 1.0)

            norm = math.sqrt(sum(v * v for v in vec.values()))
            if norm > 0:
                self.doc_vectors[repo_id] = {t: v / norm for t, v in vec.items()}
            else:
                self.doc_vectors[repo_id] = vec

    def search_semantic(
        self,
        query: str,
        category: Optional[str] = None,
        top_k: int = 8
    ) -> List[Tuple[Dict[str, Any], float]]:
        q_tokens = tokenize(query)
        if not q_tokens:
            return []

        q_tf: Dict[str, float] = {}
        for t in q_tokens:
            q_tf[t] = q_tf.get(t, 0) + 1.0

        q_vec: Dict[str, float] = {}
        for t, count in q_tf.items():
            idf = self.idf.get(t, 1.0)
            q_vec[t] = (1.0 + math.log(count)) * idf

        q_norm = math.sqrt(sum(v * v for v in q_vec.values()))
        if q_norm > 0:
            q_vec = {t: v / q_norm for t, v in q_vec.items()}

        scores = []
        for repo_id, doc_vec in self.doc_vectors.items():
            meta = self.doc_metadata[repo_id]
            if category and meta.get("category") != category:
                continue

            dot_product = sum(q_vec[t] * doc_vec[t] for t in q_vec if t in doc_vec)
            health_boost = (meta.get("health_score", 80) / 100.0) * 0.15
            final_score = dot_product + health_boost

            if dot_product > 0.05 or category:
                scores.append((meta, final_score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


class ArchitecturalConsultant:

    def __init__(self, db_path: str = DB_PATH):
        self.vector_index = SemanticVectorIndex(db_path)

    def analyze_business_intent(self, prompt: str) -> Dict[str, Any]:
        p_lower = prompt.lower()

        industry = "SaaS B2B General"
        if any(w in p_lower for w in ["logistica", "tracking", "camiones", "envios", "rutas", "bodega", "almacen"]):
            industry = "Logística & Cadena de Suministro B2B"
        elif any(w in p_lower for w in ["ecommerce", "e-commerce", "tienda", "ventas", "checkout", "catalogo", "compras"]):
            industry = "E-Commerce B2B / Marketplace"
        elif any(w in p_lower for w in ["salud", "medico", "telemedicina", "clinica", "pacientes", "recetas"]):
            industry = "HealthTech & Telemedicina"
        elif any(w in p_lower for w in ["fintech", "pagos", "banco", "facturacion", "credito", "inversion"]):
            industry = "FinTech & Facturación Recurrente"
        elif any(w in p_lower for w in ["ia", "ai", "agente", "llm", "rag", "chatbot", "inteligencia"]):
            industry = "Plataforma de IA & Agentes Autónomos"
        elif any(w in p_lower for w in ["iot", "sensores", "telemetria", "tiempo real", "dispositivos"]):
            industry = "IoT & Monitoreo en Tiempo Real"

        is_ecommerce = "ecommerce" in p_lower or "e-commerce" in p_lower or "tienda" in p_lower or "ventas" in p_lower
        is_logistics = "logistica" in p_lower or "tracking" in p_lower or "envios" in p_lower or "flota" in p_lower

        needs_auth = True
        needs_search = is_ecommerce or any(w in p_lower for w in ["buscar", "busqueda", "catalogo", "filtro", "productos", "inventario", "articulos", "instantanea"])
        needs_payments = is_ecommerce or any(w in p_lower for w in ["pago", "pagos", "factura", "facturacion", "suscripcion", "recurrente", "cobro", "tarifa"])
        needs_ai = any(w in p_lower for w in ["ia", "ai", "llm", "asistente", "inteligente", "rag", "embeddings", "modelo", "chat"])
        needs_queues = is_logistics or any(w in p_lower for w in ["realtime", "tiempo real", "tracking", "colas", "eventos", "background", "pesadas", "streaming", "notificaciones"])
        needs_notifications = is_logistics or is_ecommerce or any(w in p_lower for w in ["notificar", "notificaciones", "email", "sms", "alertas", "push", "whatsapp"])
        needs_docs = any(w in p_lower for w in ["firma", "contrato", "documento", "pdf", "acuerdo", "legal"])
        needs_cms = any(w in p_lower for w in ["cms", "contenido", "blog", "articulos", "landing", "noticias"])
        needs_crm = any(w in p_lower for w in ["crm", "leads", "clientes", "citas", "agenda", "soporte", "tickets"])

        return {
            "industry": industry,
            "layers": {
                "auth": needs_auth,
                "database": True,
                "search": needs_search or True,
                "payments": needs_payments,
                "ai": needs_ai,
                "queues": needs_queues,
                "notifications": needs_notifications,
                "documents": needs_docs,
                "cms": needs_cms,
                "crm": needs_crm,
                "observability": True,
                "devops": True
            }
        }

    def generate_recommendation(self, prompt: str) -> Dict[str, Any]:
        analysis = self.analyze_business_intent(prompt)
        layers = analysis["layers"]

        selected_components: Dict[str, Dict[str, Any]] = {}
        total_monthly_savings = 0

        def pick_component(category: str, query_hint: str) -> Optional[Dict[str, Any]]:
            results = self.vector_index.search_semantic(f"{prompt} {query_hint}", category=category, top_k=3)
            if results:
                return results[0][0]
            results = self.vector_index.search_semantic(query_hint, category=category, top_k=1)
            return results[0][0] if results else None

        auth_hint = "multi-tenant b2b sso oidc rbac" if "multi-tenant" in prompt.lower() or "b2b" in prompt.lower() else "jwt session oauth"
        auth_comp = pick_component("Autenticación", auth_hint)
        if auth_comp:
            selected_components["Autenticación & IAM"] = auth_comp

        db_hint = "postgres realtime baas" if "realtime" in prompt.lower() or "tiempo real" in prompt.lower() else "sql postgres relational"
        db_comp = pick_component("Base de Datos", db_hint)
        if db_comp:
            selected_components["Base de Datos & BaaS"] = db_comp

        if layers["search"]:
            search_hint = "instant search typo tolerance fast"
            search_comp = pick_component("Búsqueda", search_hint)
            if search_comp:
                selected_components["Motor de Búsqueda"] = search_comp

        if layers["queues"]:
            queue_hint = "streaming events queues pubsub background jobs"
            queue_comp = pick_component("Mensajería & Colas", queue_hint)
            if queue_comp:
                selected_components["Streaming & Colas"] = queue_comp

        if layers["payments"]:
            pay_hint = "metering billing subscriptions headless ecommerce"
            pay_comp = pick_component("Pagos & E-Commerce", pay_hint)
            if pay_comp:
                selected_components["Facturación & Pagos"] = pay_comp

        if layers["ai"]:
            ai_hint = "llm local inference rag agents openai proxy"
            ai_comp = pick_component("IA & LLMs", ai_hint)
            if ai_comp:
                selected_components["IA & Motor LLM"] = ai_comp

        auto_hint = "automation workflow triggers integration"
        auto_comp = pick_component("Automatización", auto_hint)
        if auto_comp:
            selected_components["Automatización & Workflows"] = auto_comp

        if layers["notifications"]:
            notif_hint = "notifications email in-app sms chat"
            notif_comp = pick_component("Notificaciones", notif_hint)
            if notif_comp:
                selected_components["Notificaciones"] = notif_comp

        if layers["documents"]:
            doc_hint = "contracts e-signature pdf"
            doc_comp = pick_component("Documentos & Firma", doc_hint)
            if doc_comp:
                selected_components["Firma & Contratos"] = doc_comp

        obs_hint = "metrics dashboards uptime monitoring opentelemetry"
        obs_comp = pick_component("Monitoreo & Logs", obs_hint)
        if obs_comp:
            selected_components["Observabilidad"] = obs_comp

        dev_hint = "self-hosted paas reverse-proxy docker deploy"
        dev_comp = pick_component("DevOps & Deploy", dev_hint)
        if dev_comp:
            selected_components["Infraestructura & Deploy"] = dev_comp

        stack_list = []
        for role, comp in selected_components.items():
            saas_cost = comp.get("estimated_monthly_saas_cost", 100)
            total_monthly_savings += saas_cost
            stack_list.append({
                "role": role,
                "id": comp["id"],
                "name": comp["name"],
                "category": comp["category"],
                "description": comp["description"],
                "health_score": comp["health_score"],
                "license": comp["license"],
                "saas_alternative": comp.get("saas_alternative", "SaaS Comercial"),
                "estimated_monthly_saas_cost": saas_cost,
                "github_url": comp["github_url"]
            })

        mermaid_chart = self._generate_mermaid_chart(selected_components)
        integration_guide = self._generate_integration_steps(selected_components, prompt)
        graph_nodes, graph_edges = self._generate_graph_data(selected_components)

        return {
            "query": prompt,
            "industry": analysis["industry"],
            "total_monthly_savings_usd": total_monthly_savings,
            "total_annual_savings_usd": total_monthly_savings * 12,
            "components_count": len(stack_list),
            "stack": stack_list,
            "mermaid_diagram": mermaid_chart,
            "graph_data": {
                "nodes": graph_nodes,
                "edges": graph_edges
            },
            "integration_guide": integration_guide,
            "executive_summary": (
                f"Para este proyecto de {analysis['industry']}, se diseñó una arquitectura de microservicios "
                f"desacoplada y altamente escalable utilizando {len(stack_list)} tecnologías open source líderes. "
                f"Esta solución elimina el vendor lock-in y representa un ahorro operativo estimado de "
                f"${total_monthly_savings:,.0f} USD/mes frente a suites de SaaS propietarias equivalentes."
            )
        }

    def _generate_mermaid_chart(self, components: Dict[str, Dict[str, Any]]) -> str:
        lines = [
            "flowchart TD",
            "    Client([Clientes Web / Mobile B2B])",
            "    Gateway[API Gateway / Reverse Proxy: Caddy o Traefik]",
            "    Client --> Gateway"
        ]

        if "Autenticación & IAM" in components:
            auth_name = components["Autenticación & IAM"]["name"]
            lines.append(f'    Auth["{auth_name} (Auth & SSO)"]')
            lines.append("    Gateway -->|Valida Token JWT| Auth")

        if "Base de Datos & BaaS" in components:
            db_name = components["Base de Datos & BaaS"]["name"]
            lines.append(f'    DB[(" {db_name} (Base de Datos Primaria) ")]')
            lines.append("    Gateway -->|Lectura / Escritura RLS| DB")

        if "Motor de Búsqueda" in components:
            s_name = components["Motor de Búsqueda"]["name"]
            lines.append(f'    Search["{s_name} (Búsqueda Rápida & Facetada)"]')
            lines.append("    Gateway -->|Búsqueda Semántica| Search")

        if "Streaming & Colas" in components:
            q_name = components["Streaming & Colas"]["name"]
            lines.append(f'    Queue["{q_name} (Colas de Tareas & Eventos)"]')
            lines.append("    Gateway -->|Encola Tareas Asíncronas| Queue")

        if "IA & Motor LLM" in components:
            ai_name = components["IA & Motor LLM"]["name"]
            lines.append(f'    AI["{ai_name} (Inferencia RAG & LLM)"]')
            lines.append("    Gateway -->|Prompt & Contexto| AI")

        if "Facturación & Pagos" in components:
            pay_name = components["Facturación & Pagos"]["name"]
            lines.append(f'    Billing["{pay_name} (Tarificación & Facturas)"]')
            lines.append("    Gateway -->|Suscripciones & Cobros| Billing")

        if "Notificaciones" in components:
            notif_name = components["Notificaciones"]["name"]
            lines.append(f'    Notif["{notif_name} (Despacho Multicanal)"]')
            if "Streaming & Colas" in components:
                lines.append("    Queue -->|Dispara Alertas| Notif")
            else:
                lines.append("    Gateway -->|Dispara Alertas| Notif")

        if "Observabilidad" in components:
            obs_name = components["Observabilidad"]["name"]
            lines.append(f'    Obs["{obs_name} (Métricas & Dashboards)"]')
            lines.append("    Gateway -.->|Telemetría & Traces| Obs")

        return "\n".join(lines)

    def _generate_graph_data(self, components: Dict[str, Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        nodes = [
            {"id": "client", "label": "Web & Mobile Clients", "type": "client", "category": "Frontend"},
            {"id": "gateway", "label": "API Gateway / Reverse Proxy", "type": "gateway", "category": "DevOps"}
        ]
        edges = [
            {"from": "client", "to": "gateway", "label": "HTTPS / WSS"}
        ]

        pos_map = {
            "Autenticación & IAM": ("auth", "Seguridad"),
            "Base de Datos & BaaS": ("database", "Datos"),
            "Motor de Búsqueda": ("search", "Búsqueda"),
            "Streaming & Colas": ("queues", "Eventos"),
            "IA & Motor LLM": ("ai", "Inteligencia"),
            "Facturación & Pagos": ("billing", "Finanzas"),
            "Notificaciones": ("notif", "Comunicación"),
            "Observabilidad": ("obs", "Monitoreo")
        }

        for role, comp in components.items():
            if role in pos_map:
                nid, cat = pos_map[role]
                nodes.append({
                    "id": nid,
                    "label": comp["name"],
                    "subtitle": role,
                    "health_score": comp["health_score"],
                    "category": cat,
                    "stars": comp.get("stars", 0)
                })
                edges.append({
                    "from": "gateway",
                    "to": nid,
                    "label": "API / gRPC"
                })

        return nodes, edges

    def _generate_integration_steps(self, components: Dict[str, Dict[str, Any]], prompt: str) -> List[Dict[str, Any]]:
        steps = []
        step_idx = 1

        if "Infraestructura & Deploy" in components:
            c = components["Infraestructura & Deploy"]
            steps.append({
                "step": step_idx,
                "title": f"Despliegue de Infraestructura Base con {c['name']}",
                "description": f"Levanta la topología de contenedores en red privada aislada utilizando {c['name']}.",
                "code": """networks:
  b2b_internal:
    driver: bridge

volumes:
  db_data:
  cache_data:
"""
            })
            step_idx += 1

        if "Autenticación & IAM" in components:
            c = components["Autenticación & IAM"]
            steps.append({
                "step": step_idx,
                "title": f"Configuración de Seguridad y Tenants con {c['name']}",
                "description": "Establece el proveedor de identidades para emitir tokens JWT con claims de tenant y roles RBAC.",
                "code": f"""import {{ verify }} from "jsonwebtoken";

export function authMiddleware(req, res, next) {{
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith("Bearer ")) return res.status(401).json({{ error: "No autorizado" }});
  
  const token = authHeader.split(" ")[1];
  const decoded = verify(token, process.env.AUTH_PUBLIC_KEY);
  req.tenantId = decoded.tenant_id;
  req.userRole = decoded.role;
  next();
}}
"""
            })
            step_idx += 1

        if "Base de Datos & BaaS" in components:
            c = components["Base de Datos & BaaS"]
            steps.append({
                "step": step_idx,
                "title": f"Persistencia de Datos y Políticas Multi-Tenant con {c['name']}",
                "description": "Crea las tablas relacionales y aplica Row Level Security (RLS) para aislar datos entre empresas clientes.",
                "code": """ALTER TABLE pedidos ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_policy ON pedidos
FOR ALL
TO authenticated
USING (tenant_id = current_setting('app.current_tenant_id', true));
"""
            })
            step_idx += 1

        if "Motor de Búsqueda" in components and "Base de Datos & BaaS" in components:
            s = components["Motor de Búsqueda"]
            steps.append({
                "step": step_idx,
                "title": f"Sincronización de Catálogo hacia {s['name']}",
                "description": f"Replica los registros actualizados de la base de datos hacia el motor {s['name']} para consultas instantáneas.",
                "code": f"""export async function onProductUpdated(product) {{
  await meiliClient.index("catalogo").addDocuments([{{
    id: product.id,
    sku: product.sku,
    nombre: product.nombre,
    precio: product.precio,
    categoria: product.categoria,
    tenant_id: product.tenant_id
  }}]);
}}
"""
            })
            step_idx += 1

        if "Streaming & Colas" in components:
            q = components["Streaming & Colas"]
            steps.append({
                "step": step_idx,
                "title": f"Manejo de Cargas Pesadas y Eventos con {q['name']}",
                "description": "Desacopla tareas que requieren tiempo (reportes, PDFs, sincronizaciones externas) mediante colas resilientes.",
                "code": """import pika

def procesar_tarea(ch, method, properties, body):
    print("Ejecutando proceso pesado:", body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)
"""
            })
            step_idx += 1

        return steps
