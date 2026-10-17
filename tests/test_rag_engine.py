"""
Pruebas unitarias para el motor RAG de recomendación arquitectónica.
"""

import unittest
from backend.rag_engine import ArchitecturalConsultant, tokenize


class TestRAGEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.consultant = ArchitecturalConsultant()

    def test_tokenization_and_stopwords(self):
        tokens = tokenize("Estoy construyendo un E-Commerce B2B con PostgreSQL!")
        self.assertIn("ecommerce", [t.replace("-", "") for t in tokens])
        self.assertIn("b2b", tokens)
        self.assertIn("postgresql", tokens)
        self.assertNotIn("un", tokens)
        self.assertNotIn("con", tokens)

    def test_business_intent_analysis(self):
        analysis = self.consultant.analyze_business_intent("E-commerce de repuestos con pasarela de pagos")
        self.assertIn("E-Commerce", analysis["industry"])
        self.assertTrue(analysis["layers"]["payments"])
        self.assertTrue(analysis["layers"]["auth"])

    def test_architecture_recommendation_generation(self):
        prompt = "Estoy construyendo un e-commerce B2B de logística con tracking en tiempo real"
        result = self.consultant.generate_recommendation(prompt)

        self.assertIn("industry", result)
        self.assertGreater(result["total_monthly_savings_usd"], 500)
        self.assertGreater(result["components_count"], 3)
        self.assertIn("flowchart", result["mermaid_diagram"])
        self.assertIn("nodes", result["graph_data"])
        self.assertGreater(len(result["integration_guide"]), 0)


if __name__ == "__main__":
    unittest.main()
