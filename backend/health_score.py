"""
Algoritmo de cálculo de Health Score y nivel de mantenimiento para repositorios open source.
Pondera frescura de commits, actividad de issues/forks, comunidad y licencia.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Tuple


def calculate_health_score(repo_data: Dict[str, Any]) -> Tuple[int, str]:
    """
    Calcula el Health Score (0 - 100) y clasifica el nivel de mantenimiento.
    
    Ponderaciones:
    - Frescura de commits / actividad (hasta 35 pts)
    - Proporción de issues abiertos vs forks y estrellas (hasta 25 pts)
    - Adopción y comunidad (estrellas y forks) (hasta 20 pts)
    - Licencia permisiva / amigable para empresas (hasta 10 pts)
    - Mantenedor activo declarado (hasta 10 pts)
    """
    score = 0

    # 1. Frescura de commits (35 pts)
    last_updated_str = repo_data.get("last_updated")
    if last_updated_str:
        try:
            if last_updated_str.endswith("Z"):
                last_updated_str = last_updated_str[:-1] + "+00:00"
            last_date = datetime.fromisoformat(last_updated_str)
            now = datetime.now(timezone.utc)
            days_diff = max(0, (now - last_date).days)

            if days_diff <= 14:
                score += 35
            elif days_diff <= 45:
                score += 30
            elif days_diff <= 90:
                score += 22
            elif days_diff <= 180:
                score += 15
            elif days_diff <= 365:
                score += 8
            else:
                score += 2
        except Exception:
            score += 20
    else:
        score += 15

    # 2. Ratio y salud de issues (25 pts)
    stars = repo_data.get("stars", 0)
    forks = repo_data.get("forks", 0)
    open_issues = repo_data.get("open_issues", 0)
    
    total_activity = max(1, stars + forks)
    issue_ratio = open_issues / total_activity

    if issue_ratio < 0.03:
        score += 25
    elif issue_ratio < 0.08:
        score += 20
    elif issue_ratio < 0.15:
        score += 15
    elif issue_ratio < 0.30:
        score += 10
    else:
        score += 5

    # 3. Adopción comunitaria (20 pts)
    if stars >= 40000:
        score += 20
    elif stars >= 20000:
        score += 17
    elif stars >= 8000:
        score += 14
    elif stars >= 2000:
        score += 10
    elif stars >= 500:
        score += 6
    else:
        score += 3

    # 4. Licencia empresarial amigable (10 pts)
    lic = (repo_data.get("license") or "").upper()
    if any(p in lic for p in ["MIT", "APACHE", "BSD", "ISC"]):
        score += 10
    elif any(p in lic for p in ["MPL", "POSTGRESQL", "ZLIB"]):
        score += 8
    elif any(p in lic for p in ["AGPL", "GPL", "BSL"]):
        score += 6
    else:
        score += 4

    # 5. Mantenedor activo (10 pts)
    if repo_data.get("active_maintainer", True):
        score += 10
    else:
        score += 0

    final_score = min(100, max(0, score))

    # Determinar categoría de mantenimiento
    if final_score >= 90:
        level = "Excelente"
    elif final_score >= 75:
        level = "Activo"
    elif final_score >= 55:
        level = "Mantenimiento Bajo"
    else:
        level = "En Riesgo"

    return final_score, level
