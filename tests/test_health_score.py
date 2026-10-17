"""
Pruebas unitarias para el algoritmo de cálculo de Health Score y niveles de mantenimiento.
"""

import unittest
from backend.health_score import calculate_health_score


class TestHealthScore(unittest.TestCase):

    def test_high_health_repository(self):
        repo = {
            "name": "SuperProject",
            "stars": 50000,
            "forks": 5000,
            "open_issues": 100,
            "last_updated": "2026-10-15T12:00:00Z",
            "license": "MIT",
            "active_maintainer": True
        }
        score, level = calculate_health_score(repo)
        self.assertGreaterEqual(score, 90)
        self.assertEqual(level, "Excelente")

    def test_stale_repository(self):
        repo = {
            "name": "OldProject",
            "stars": 500,
            "forks": 50,
            "open_issues": 300,
            "last_updated": "2023-01-01T00:00:00Z",
            "license": "GPL-2.0",
            "active_maintainer": False
        }
        score, level = calculate_health_score(repo)
        self.assertLess(score, 60)
        self.assertIn(level, ["Mantenimiento Bajo", "En Riesgo"])


if __name__ == "__main__":
    unittest.main()
