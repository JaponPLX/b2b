"""
Pruebas unitarias para persistencia y gestion de blueprints de clientes.
"""

import unittest
import os
import json
from backend.database import (
    init_db, save_blueprint, get_saved_blueprints,
    get_saved_blueprint_by_id, delete_saved_blueprint
)

TEST_DB = os.path.join(os.path.dirname(__file__), "test_blueprints.db")


class TestBlueprintsPersistence(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        init_db(TEST_DB)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_save_and_retrieve_blueprint(self):
        sample_data = {
            "industry": "FinTech / Pagos",
            "executive_summary": "Arquitectura distribuida con Postgres, RabbitMQ y Keycloak.",
            "total_monthly_savings_usd": 2400,
            "total_annual_savings_usd": 28800,
            "query": "Plataforma de pagos multi-tenant para bancos",
            "stack": [
                {
                    "name": "Supabase",
                    "role": "Base de datos & Auth",
                    "saas_alternative": "Firebase / Auth0",
                    "estimated_monthly_saas_cost": 450,
                    "health_score": 96
                }
            ],
            "sizing_estimate": {
                "ram_gb": 16,
                "cpu_cores": 8,
                "storage_gb": 120,
                "vps_monthly_cost_usd": 48,
                "net_monthly_savings_usd": 2352
            }
        }

        bp_id = save_blueprint(
            client_name="Banco Digital SAS",
            data=sample_data,
            project_title="Core Bancario Open Source",
            industry="FinTech",
            db_path=TEST_DB
        )

        self.assertTrue(bp_id.startswith("bp_"))

        # Fetch all
        items = get_saved_blueprints(db_path=TEST_DB)
        self.assertGreaterEqual(len(items), 1)
        found = next((b for b in items if b["id"] == bp_id), None)
        self.assertIsNotNone(found)
        self.assertEqual(found["client_name"], "Banco Digital SAS")
        self.assertEqual(found["total_monthly_savings"], 2400)

        # Fetch by ID
        single = get_saved_blueprint_by_id(bp_id, db_path=TEST_DB)
        self.assertIsNotNone(single)
        self.assertEqual(single["client_name"], "Banco Digital SAS")
        self.assertIn("data", single)
        self.assertEqual(single["data"]["industry"], "FinTech / Pagos")
        self.assertEqual(single["data"]["sizing_estimate"]["ram_gb"], 16)

        # Delete
        deleted = delete_saved_blueprint(bp_id, db_path=TEST_DB)
        self.assertTrue(deleted)

        after_delete = get_saved_blueprint_by_id(bp_id, db_path=TEST_DB)
        self.assertIsNone(after_delete)

    def test_get_local_ip(self):
        from backend.app import get_local_ip
        ip = get_local_ip()
        self.assertIsInstance(ip, str)
        self.assertGreater(len(ip), 0)


if __name__ == "__main__":
    unittest.main()

