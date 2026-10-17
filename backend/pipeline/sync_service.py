"""
Servicio automatizado de ingesta y sincronización periódica de repositorios.
Procesa repositorios en lotes priorizados, actualiza metadatos y recalcula el Health Score.
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Dict, Any, List
from backend.database import get_db_connection, upsert_repository, record_sync_log, DB_PATH
from backend.pipeline.github_client import GitHubClient
from backend.health_score import calculate_health_score


class IngestionPipeline:

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.client = GitHubClient()

    def run_sync_batch(self, limit: int = 15) -> Dict[str, Any]:
        conn = get_db_connection(self.db_path)
        cur = conn.cursor()
        cur.execute("""
        SELECT id, name, full_name, category, description, stars, forks, open_issues,
               last_updated, license, language, website_url, github_url, docs_url,
               saas_alternative, estimated_monthly_saas_cost, tags_json
        FROM repositories
        ORDER BY updated_at ASC, stars DESC
        LIMIT ?
        """, (limit,))
        candidates = [dict(r) for r in cur.fetchall()]
        conn.close()

        checked = 0
        updated = 0
        details = []

        for repo in candidates:
            full_name = repo.get("full_name")
            if not full_name:
                continue

            checked += 1
            fresh_data, rate_limit = self.client.fetch_repo_data(full_name)

            if fresh_data:
                if fresh_data.get("simulated"):
                    repo["stars"] = repo.get("stars", 0) + fresh_data.get("stars_delta", 2)
                    repo["last_updated"] = fresh_data.get("last_updated")
                else:
                    repo["stars"] = fresh_data.get("stars", repo.get("stars", 0))
                    repo["forks"] = fresh_data.get("forks", repo.get("forks", 0))
                    repo["open_issues"] = fresh_data.get("open_issues", repo.get("open_issues", 0))
                    repo["last_updated"] = fresh_data.get("last_updated", repo.get("last_updated"))
                    if fresh_data.get("license"):
                        repo["license"] = fresh_data["license"]

                score, level = calculate_health_score(repo)
                repo["health_score"] = score
                repo["maintenance_level"] = level

                upsert_repository(repo, db_path=self.db_path)
                updated += 1
                details.append(f"{repo['name']}: score={score}, stars={repo['stars']}")

        status = "OK" if updated > 0 else "SIN_CAMBIOS"
        summary_msg = f"Sincronizados {updated}/{checked} repositorios. Rate-limit restante: {self.client.rate_limit_remaining}"
        record_sync_log(checked, updated, self.client.rate_limit_remaining, status, summary_msg, db_path=self.db_path)

        return {
            "status": status,
            "checked": checked,
            "updated": updated,
            "rate_limit_remaining": self.client.rate_limit_remaining,
            "message": summary_msg,
            "details": details
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline de sincronización con GitHub API")
    parser.add_argument("--limit", type=int, default=10, help="Número de repositorios a sincronizar en este lote")
    args = parser.parse_args()

    pipeline = IngestionPipeline()
    result = pipeline.run_sync_batch(limit=args.limit)
    print(f"[{result['status']}] {result['message']}")
    for d in result["details"]:
        print(f"  - {d}")
