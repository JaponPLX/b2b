"""
Servidor REST API principal en Python para el Acelerador de Integraciones Open Source.
Ofrece endpoints para búsqueda, filtros, recomendaciones RAG y sincronización de datos.
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import sys
import mimetypes

# Asegurar que la raíz del proyecto esté en el path de Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any

from backend.database import (
    init_db, seed_if_empty, get_repositories, get_repo_by_id,
    get_categories_summary, get_filter_options, get_stats_summary,
    get_recent_sync_logs, DB_PATH
)
from backend.rag_engine import ArchitecturalConsultant
from backend.pipeline.sync_service import IngestionPipeline

PORT = int(os.getenv("PORT", 8080))
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")


class B2BCatalogHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def _send_json_response(self, data: Any, status_code: int = 200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)

        if path == "/api/repos":
            q = query_params.get("q", [None])[0]
            category = query_params.get("category", [None])[0]
            language = query_params.get("language", [None])[0]
            license_type = query_params.get("license", [None])[0]
            maintenance = query_params.get("maintenance", [None])[0]
            min_stars = query_params.get("min_stars", [None])[0]
            sort_by = query_params.get("sort_by", ["stars_desc"])[0]
            limit = int(query_params.get("limit", [50])[0])
            offset = int(query_params.get("offset", [0])[0])

            repos, total = get_repositories(
                query=q,
                category=category,
                language=language,
                license_type=license_type,
                maintenance_level=maintenance,
                min_stars=int(min_stars) if min_stars else None,
                sort_by=sort_by,
                limit=limit,
                offset=offset
            )
            return self._send_json_response({
                "total": total,
                "limit": limit,
                "offset": offset,
                "items": repos
            })

        # Comparación de repositorios (debe ir antes de /api/repos/:id)
        if path == "/api/repos/compare":
            ids_param = query_params.get("ids", [""])[0]
            id_list = [i.strip() for i in ids_param.split(",") if i.strip()]
            from backend.database import get_repos_by_ids
            repos = get_repos_by_ids(id_list)
            return self._send_json_response({"items": repos})

        if path.startswith("/api/repos/"):
            repo_id = path.replace("/api/repos/", "").strip("/")
            repo = get_repo_by_id(repo_id)
            if repo:
                return self._send_json_response(repo)
            return self._send_json_response({"error": "Repositorio no encontrado"}, status_code=404)

        if path == "/api/categories":
            return self._send_json_response(get_categories_summary())

        if path == "/api/filters":
            return self._send_json_response(get_filter_options())

        if path == "/api/stats":
            return self._send_json_response(get_stats_summary())

        # 7. API: Logs de sincronización
        if path == "/api/pipeline/logs":
            return self._send_json_response(get_recent_sync_logs(limit=20))

        if path == "/" or not os.path.exists(os.path.join(FRONTEND_DIR, path.lstrip("/"))):
            self.path = "/index.html"
            return super().do_GET()

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body_raw = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            payload = json.loads(body_raw) if body_raw else {}
        except Exception:
            payload = {}

        # 1. API: Asistente Consultor de Arquitectura RAG
        if path == "/api/rag/recommend":
            prompt = payload.get("prompt", "").strip()
            if not prompt:
                return self._send_json_response(
                    {"error": "Debes ingresar una descripción de negocio o producto."},
                    status_code=400
                )

            consultant = ArchitecturalConsultant()
            recommendation = consultant.generate_recommendation(prompt)
            return self._send_json_response(recommendation)

        # 2. API: Agregar nuevo repositorio en vivo
        if path == "/api/repos/add":
            full_name = payload.get("full_name", "").strip().lower()
            if not full_name or "/" not in full_name:
                return self._send_json_response({"error": "Formato inválido. Debe ser 'owner/repo' (ej: supabase/supabase)."}, status_code=400)

            slug = full_name.split("/")[1]
            from backend.pipeline.github_client import GitHubClient
            from backend.health_score import calculate_health_score
            from backend.database import upsert_repository, get_repo_by_id, get_db_connection

            client = GitHubClient()
            data, remaining = client.fetch_repo_data(full_name)
            if not data:
                return self._send_json_response({"error": f"No se pudo consultar el repositorio {full_name} en GitHub."}, status_code=404)

            repo_dict = {
                "id": slug,
                "name": payload.get("name") or data.get("name") or slug.capitalize(),
                "full_name": full_name,
                "category": payload.get("category") or "DevOps & Deploy",
                "description": data.get("description") or payload.get("description") or "Herramienta open source.",
                "stars": data.get("stars", 1000),
                "forks": data.get("forks", 100),
                "open_issues": data.get("open_issues", 20),
                "last_updated": data.get("last_updated"),
                "license": data.get("license") or "MIT",
                "language": data.get("language") or "TypeScript",
                "active_maintainer": True,
                "website_url": data.get("website_url") or f"https://github.com/{full_name}",
                "github_url": f"https://github.com/{full_name}",
                "docs_url": f"https://github.com/{full_name}#readme",
                "saas_alternative": payload.get("saas_alternative") or "SaaS Propietario",
                "estimated_monthly_saas_cost": int(payload.get("estimated_monthly_saas_cost", 120)),
                "tags": [data.get("language", "dev").lower(), slug, "open-source"]
            }

            score, level = calculate_health_score(repo_dict)
            repo_dict["health_score"] = score
            repo_dict["maintenance_level"] = level
            upsert_repository(repo_dict)

            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
            INSERT OR REPLACE INTO integrations (
                id, repo_id, title, integration_type, stack_compatibility_json,
                difficulty, triggers_webhooks, code_snippet, dependencies_json,
                docs_link, explanation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"{slug}_integ_1",
                slug,
                f"Integración con {repo_dict['name']}",
                "Docker / SDK",
                json.dumps(["Docker", repo_dict["language"]]),
                "Fácil",
                "Eventos del sistema",
                f"# Despliegue de {repo_dict['name']}\ndocker run -d --name {slug}-service -p 8080:8080 {slug}:latest",
                json.dumps([f"{slug}-client"]),
                repo_dict["docs_url"],
                f"Permite desplegar e integrar {repo_dict['name']} en tu arquitectura B2B."
            ))
            conn.commit()
            conn.close()

            saved = get_repo_by_id(slug)
            return self._send_json_response({"message": f"Repositorio {full_name} analizado y agregado con éxito.", "repo": saved})

        # 3. API: Disparar sincronización con GitHub API
        if path == "/api/pipeline/sync":
            limit = int(payload.get("limit", 10))
            pipeline = IngestionPipeline()
            result = pipeline.run_sync_batch(limit=limit)
            return self._send_json_response(result)

        return self._send_json_response({"error": "Endpoint no encontrado"}, status_code=404)


def run_server(port: int = PORT):
    init_db()
    count = seed_if_empty()
    print(f"Base de datos lista con {count} repositorios.")
    print(f"Servidor iniciado en http://localhost:{port}")

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), B2BCatalogHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")


if __name__ == "__main__":
    run_server()
