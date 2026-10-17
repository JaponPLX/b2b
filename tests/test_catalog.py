"""
Pruebas unitarias para el catálogo de tecnologías, persistencia SQLite y FTS5.
"""

import unittest
import os
from backend.database import (
    init_db, seed_if_empty, get_repositories, get_repo_by_id,
    get_categories_summary, get_filter_options, get_stats_summary
)

TEST_DB = os.path.join(os.path.dirname(__file__), "test_catalog.db")


class TestCatalogDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        init_db(TEST_DB)
        cls.count = seed_if_empty(TEST_DB)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_database_has_over_100_repositories(self):
        self.assertGreaterEqual(self.count, 100, f"Debe tener >= 100 repositorios, encontrados {self.count}")

    def test_fts5_search_query(self):
        items, total = get_repositories(query="postgres", db_path=TEST_DB)
        self.assertGreater(total, 0)
        names = [r["name"].lower() for r in items]
        self.assertTrue(any("supabase" in n or "postgres" in n or "prisma" in n for n in names))

    def test_filter_by_category(self):
        items, total = get_repositories(category="Autenticación", db_path=TEST_DB)
        self.assertGreater(total, 0)
        for r in items:
            self.assertEqual(r["category"], "Autenticación")

    def test_filter_by_min_stars(self):
        min_stars = 20000
        items, total = get_repositories(min_stars=min_stars, db_path=TEST_DB)
        self.assertGreater(total, 0)
        for r in items:
            self.assertGreaterEqual(r["stars"], min_stars)

    def test_get_repo_by_id_with_integrations(self):
        repo = get_repo_by_id("supabase", db_path=TEST_DB)
        self.assertIsNotNone(repo)
        self.assertEqual(repo["id"], "supabase")
        self.assertIn("integrations", repo)
        self.assertGreater(len(repo["integrations"]), 0)
        integ = repo["integrations"][0]
        self.assertIn("code_snippet", integ)
        self.assertIn("integration_type", integ)

    def test_categories_and_stats(self):
        cats = get_categories_summary(db_path=TEST_DB)
        self.assertGreater(len(cats), 5)
        stats = get_stats_summary(db_path=TEST_DB)
        self.assertGreaterEqual(stats["total_repos"], 100)
        self.assertGreater(stats["total_saas_savings"], 5000)

    def test_get_repos_by_ids_comparison(self):
        from backend.database import get_repos_by_ids
        repos = get_repos_by_ids(["supabase", "strapi", "redis"], db_path=TEST_DB)
        self.assertEqual(len(repos), 3)
        ids = [r["id"] for r in repos]
        self.assertIn("supabase", ids)
        self.assertIn("strapi", ids)
        self.assertIn("redis", ids)
        for r in repos:
            self.assertIn("integrations", r)
            self.assertIn("health_score", r)


if __name__ == "__main__":
    unittest.main()
