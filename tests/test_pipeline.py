"""
Pruebas unitarias para el pipeline de ingesta y cliente GitHub API.
"""

import unittest
from backend.pipeline.github_client import GitHubClient
from backend.pipeline.sync_service import IngestionPipeline


class TestPipeline(unittest.TestCase):

    def test_github_client_token_rotation(self):
        client = GitHubClient(tokens=["tok_1", "tok_2"])
        t1 = client._get_active_token()
        t2 = client._get_active_token()
        t3 = client._get_active_token()
        self.assertEqual(t1, "tok_1")
        self.assertEqual(t2, "tok_2")
        self.assertEqual(t3, "tok_1")

    def test_pipeline_sync_execution(self):
        pipeline = IngestionPipeline()
        result = pipeline.run_sync_batch(limit=3)
        self.assertIn("status", result)
        self.assertEqual(result["checked"], 3)
        self.assertGreaterEqual(result["updated"], 1)


if __name__ == "__main__":
    unittest.main()
