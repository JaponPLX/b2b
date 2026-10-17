"""
Capa de persistencia SQLite con soporte FTS5 para búsqueda full-text y consultas relacionales.
"""

import sqlite3
import json
import os
from typing import List, Dict, Any, Optional, Tuple
from backend.health_score import calculate_health_score
from backend.seed_data import build_complete_catalog

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "catalog.db")


def get_db_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: str = DB_PATH):
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS repositories (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        full_name TEXT NOT NULL UNIQUE,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        stars INTEGER NOT NULL DEFAULT 0,
        forks INTEGER NOT NULL DEFAULT 0,
        open_issues INTEGER NOT NULL DEFAULT 0,
        last_updated TEXT,
        license TEXT NOT NULL,
        language TEXT NOT NULL,
        health_score INTEGER NOT NULL DEFAULT 0,
        maintenance_level TEXT NOT NULL,
        active_maintainer INTEGER NOT NULL DEFAULT 1,
        website_url TEXT,
        github_url TEXT NOT NULL,
        docs_url TEXT,
        saas_alternative TEXT,
        estimated_monthly_saas_cost INTEGER DEFAULT 0,
        tags_json TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS integrations (
        id TEXT PRIMARY KEY,
        repo_id TEXT NOT NULL,
        title TEXT NOT NULL,
        integration_type TEXT NOT NULL,
        stack_compatibility_json TEXT,
        difficulty TEXT NOT NULL,
        triggers_webhooks TEXT,
        code_snippet TEXT NOT NULL,
        dependencies_json TEXT,
        docs_link TEXT,
        explanation TEXT,
        FOREIGN KEY (repo_id) REFERENCES repositories(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS sync_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        repos_checked INTEGER DEFAULT 0,
        repos_updated INTEGER DEFAULT 0,
        rate_limit_remaining INTEGER DEFAULT 0,
        status TEXT NOT NULL,
        details TEXT
    );

    CREATE VIRTUAL TABLE IF NOT EXISTS repos_fts USING fts5(
        id UNINDEXED,
        name,
        full_name,
        category,
        description,
        tags,
        language,
        content='repositories',
        content_rowid='rowid'
    );
    """)

    cur.executescript("""
    CREATE TRIGGER IF NOT EXISTS repos_ai AFTER INSERT ON repositories BEGIN
        INSERT INTO repos_fts(rowid, id, name, full_name, category, description, tags, language)
        VALUES (new.rowid, new.id, new.name, new.full_name, new.category, new.description, new.tags_json, new.language);
    END;

    CREATE TRIGGER IF NOT EXISTS repos_ad AFTER DELETE ON repositories BEGIN
        INSERT INTO repos_fts(repos_fts, rowid, id, name, full_name, category, description, tags, language)
        VALUES('delete', old.rowid, old.id, old.name, old.full_name, old.category, old.description, old.tags_json, old.language);
    END;

    CREATE TRIGGER IF NOT EXISTS repos_au AFTER UPDATE ON repositories BEGIN
        INSERT INTO repos_fts(repos_fts, rowid, id, name, full_name, category, description, tags, language)
        VALUES('delete', old.rowid, old.id, old.name, old.full_name, old.category, old.description, old.tags_json, old.language);
        INSERT INTO repos_fts(rowid, id, name, full_name, category, description, tags, language)
        VALUES (new.rowid, new.id, new.name, new.full_name, new.category, new.description, new.tags_json, new.language);
    END;
    """)

    conn.commit()
    conn.close()


def seed_if_empty(db_path: str = DB_PATH) -> int:
    conn = get_db_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM repositories")
    count = cur.fetchone()[0]

    if count > 0:
        conn.close()
        return count

    catalog = build_complete_catalog()
    for repo in catalog:
        if "health_score" not in repo or repo["health_score"] == 0:
            score, level = calculate_health_score(repo)
            repo["health_score"] = score
            repo["maintenance_level"] = level

        cur.execute("""
        INSERT INTO repositories (
            id, name, full_name, category, description, stars, forks, open_issues,
            last_updated, license, language, health_score, maintenance_level,
            active_maintainer, website_url, github_url, docs_url,
            saas_alternative, estimated_monthly_saas_cost, tags_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            repo["id"],
            repo["name"],
            repo["full_name"],
            repo["category"],
            repo["description"],
            repo.get("stars", 0),
            repo.get("forks", 0),
            repo.get("open_issues", 0),
            repo.get("last_updated"),
            repo.get("license", "MIT"),
            repo.get("language", "TypeScript"),
            repo["health_score"],
            repo["maintenance_level"],
            1 if repo.get("active_maintainer", True) else 0,
            repo.get("website_url"),
            repo.get("github_url"),
            repo.get("docs_url"),
            repo.get("saas_alternative"),
            repo.get("estimated_monthly_saas_cost", 0),
            json.dumps(repo.get("tags", []))
        ))

        integ = repo.get("integration")
        if integ:
            cur.execute("""
            INSERT INTO integrations (
                id, repo_id, title, integration_type, stack_compatibility_json,
                difficulty, triggers_webhooks, code_snippet, dependencies_json,
                docs_link, explanation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"{repo['id']}_integ_1",
                repo["id"],
                integ.get("title", f"Integración con {repo['name']}"),
                integ.get("integration_type", "SDK"),
                json.dumps(integ.get("stack_compatibility", ["Node.js"])),
                integ.get("difficulty", "Fácil"),
                integ.get("triggers_webhooks", ""),
                integ.get("code_snippet", ""),
                json.dumps(integ.get("dependencies", [])),
                integ.get("docs_link", repo.get("docs_url", "")),
                integ.get("explanation", "")
            ))

    conn.commit()
    cur.execute("SELECT COUNT(*) FROM repositories")
    inserted_count = cur.fetchone()[0]
    conn.close()
    return inserted_count


def get_repositories(
    query: Optional[str] = None,
    category: Optional[str] = None,
    language: Optional[str] = None,
    license_type: Optional[str] = None,
    maintenance_level: Optional[str] = None,
    min_stars: Optional[int] = None,
    sort_by: str = "stars_desc",
    limit: int = 50,
    offset: int = 0,
    db_path: str = DB_PATH
) -> Tuple[List[Dict[str, Any]], int]:
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    conditions = []
    params = []

    if query and query.strip():
        clean_q = "".join(c for c in query.strip() if c.isalnum() or c in (" ", "-", "_"))
        words = clean_q.split()
        if words:
            fts_query = " ".join(f'"{w}"*' for w in words)
            conditions.append("r.rowid IN (SELECT rowid FROM repos_fts WHERE repos_fts MATCH ?)")
            params.append(fts_query)

    if category and category != "all":
        conditions.append("r.category = ?")
        params.append(category)

    if language and language != "all":
        conditions.append("r.language = ?")
        params.append(language)

    if license_type and license_type != "all":
        conditions.append("r.license LIKE ?")
        params.append(f"%{license_type}%")

    if maintenance_level and maintenance_level != "all":
        conditions.append("r.maintenance_level = ?")
        params.append(maintenance_level)

    if min_stars and int(min_stars) > 0:
        conditions.append("r.stars >= ?")
        params.append(int(min_stars))

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""

    sort_map = {
        "stars_desc": "r.stars DESC",
        "stars_asc": "r.stars ASC",
        "health_desc": "r.health_score DESC",
        "name_asc": "r.name ASC",
        "updated_desc": "r.last_updated DESC"
    }
    order_clause = f" ORDER BY {sort_map.get(sort_by, 'r.stars DESC')}"

    count_sql = f"SELECT COUNT(*) FROM repositories r {where_clause}"
    cur.execute(count_sql, params)
    total_count = cur.fetchone()[0]

    sql = f"""
    SELECT r.*, 
           i.title as integ_title, 
           i.integration_type as integ_type, 
           i.difficulty as integ_difficulty
    FROM repositories r
    LEFT JOIN integrations i ON r.id = i.repo_id
    {where_clause}
    {order_clause}
    LIMIT ? OFFSET ?
    """
    cur.execute(sql, params + [limit, offset])
    rows = cur.fetchall()

    results = []
    for row in rows:
        d = dict(row)
        d["tags"] = json.loads(d.get("tags_json") or "[]")
        results.append(d)

    conn.close()
    return results, total_count


def get_repo_by_id(repo_id: str, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    cur.execute("SELECT * FROM repositories WHERE id = ?", (repo_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return None

    repo_data = dict(row)
    repo_data["tags"] = json.loads(repo_data.get("tags_json") or "[]")

    cur.execute("SELECT * FROM integrations WHERE repo_id = ?", (repo_id,))
    integs = []
    for i_row in cur.fetchall():
        idict = dict(i_row)
        idict["stack_compatibility"] = json.loads(idict.get("stack_compatibility_json") or "[]")
        idict["dependencies"] = json.loads(idict.get("dependencies_json") or "[]")
        integs.append(idict)

    repo_data["integrations"] = integs
    conn.close()
    return repo_data


def get_repos_by_ids(repo_ids: List[str], db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Obtiene múltiples repositorios para comparación lado a lado."""
    if not repo_ids:
        return []
    conn = get_db_connection(db_path)
    cur = conn.cursor()
    placeholders = ",".join("?" for _ in repo_ids)
    cur.execute(f"SELECT * FROM repositories WHERE id IN ({placeholders})", repo_ids)
    rows = cur.fetchall()
    results = []
    for row in rows:
        d = dict(row)
        d["tags"] = json.loads(d.get("tags_json") or "[]")
        # Obtener integraciones
        cur.execute("SELECT * FROM integrations WHERE repo_id = ?", (d["id"],))
        integs = []
        for i_row in cur.fetchall():
            idict = dict(i_row)
            idict["stack_compatibility"] = json.loads(idict.get("stack_compatibility_json") or "[]")
            integs.append(idict)
        d["integrations"] = integs
        results.append(d)
    conn.close()
    return results


def get_categories_summary(db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    conn = get_db_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
    SELECT category, COUNT(*) as count, AVG(health_score) as avg_health, SUM(stars) as total_stars
    FROM repositories
    GROUP BY category
    ORDER BY count DESC
    """)
    rows = cur.fetchall()
    summary = [dict(r) for r in rows]
    conn.close()
    return summary


def get_filter_options(db_path: str = DB_PATH) -> Dict[str, Any]:
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT language FROM repositories WHERE language IS NOT NULL ORDER BY language ASC")
    languages = [r[0] for r in cur.fetchall()]

    cur.execute("SELECT DISTINCT license FROM repositories WHERE license IS NOT NULL ORDER BY license ASC")
    licenses = [r[0] for r in cur.fetchall()]

    cur.execute("SELECT DISTINCT category FROM repositories WHERE category IS NOT NULL ORDER BY category ASC")
    categories = [r[0] for r in cur.fetchall()]

    conn.close()
    return {
        "categories": categories,
        "languages": languages,
        "licenses": licenses,
        "maintenance_levels": ["Excelente", "Activo", "Mantenimiento Bajo", "En Riesgo"],
        "star_ranges": [
            {"label": "Todas las estrellas", "value": 0},
            {"label": "★ 5k+", "value": 5000},
            {"label": "★ 15k+", "value": 15000},
            {"label": "★ 30k+", "value": 30000},
            {"label": "★ 50k+", "value": 50000}
        ]
    }


def get_stats_summary(db_path: str = DB_PATH) -> Dict[str, Any]:
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    cur.execute("""
    SELECT 
        COUNT(*) as total_repos,
        AVG(health_score) as avg_health,
        SUM(stars) as total_stars,
        COUNT(DISTINCT category) as total_categories,
        SUM(estimated_monthly_saas_cost) as total_saas_savings
    FROM repositories
    """)
    row = cur.fetchone()
    stats = dict(row) if row else {}

    cur.execute("SELECT COUNT(*) FROM integrations")
    stats["total_integrations"] = cur.fetchone()[0]

    cur.execute("""
    SELECT maintenance_level, COUNT(*) as count 
    FROM repositories 
    GROUP BY maintenance_level
    """)
    stats["maintenance_distribution"] = {r[0]: r[1] for r in cur.fetchall()}

    conn.close()
    return stats


def upsert_repository(repo: Dict[str, Any], db_path: str = DB_PATH):
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    score, level = calculate_health_score(repo)

    cur.execute("""
    INSERT INTO repositories (
        id, name, full_name, category, description, stars, forks, open_issues,
        last_updated, license, language, health_score, maintenance_level,
        active_maintainer, website_url, github_url, docs_url,
        saas_alternative, estimated_monthly_saas_cost, tags_json, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(id) DO UPDATE SET
        stars = excluded.stars,
        forks = excluded.forks,
        open_issues = excluded.open_issues,
        last_updated = excluded.last_updated,
        health_score = excluded.health_score,
        maintenance_level = excluded.maintenance_level,
        updated_at = CURRENT_TIMESTAMP
    """, (
        repo["id"],
        repo["name"],
        repo["full_name"],
        repo["category"],
        repo["description"],
        repo.get("stars", 0),
        repo.get("forks", 0),
        repo.get("open_issues", 0),
        repo.get("last_updated"),
        repo.get("license", "MIT"),
        repo.get("language", "TypeScript"),
        score,
        level,
        1 if repo.get("active_maintainer", True) else 0,
        repo.get("website_url"),
        repo.get("github_url"),
        repo.get("docs_url"),
        repo.get("saas_alternative"),
        repo.get("estimated_monthly_saas_cost", 0),
        json.dumps(repo.get("tags", []))
    ))

    conn.commit()
    conn.close()


def record_sync_log(checked: int, updated: int, rate_limit: int, status: str, details: str, db_path: str = DB_PATH):
    conn = get_db_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO sync_logs (repos_checked, repos_updated, rate_limit_remaining, status, details)
    VALUES (?, ?, ?, ?, ?)
    """, (checked, updated, rate_limit, status, details))
    conn.commit()
    conn.close()


def get_recent_sync_logs(limit: int = 10, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    conn = get_db_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sync_logs ORDER BY id DESC LIMIT ?", (limit,))
    logs = [dict(r) for r in cur.fetchall()]
    conn.close()
    return logs
