import unittest

from fastapi.testclient import TestClient

from nabazhome_luckfox.api.app import create_app
from nabazhome_luckfox.config.settings import Settings


class DashboardApiTests(unittest.TestCase):
    def test_dashboard_device_starts_ready(self):
        app = create_app(Settings(debug=True))
        client = TestClient(app)

        response = client.get('/api/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['device']['status'], 'ready')

    def test_dashboard_endpoint_returns_aggregated_summary(self):
        app = create_app(Settings(debug=True))
        client = TestClient(app)

        response = client.get('/api/dashboard')
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn('device', payload)
        self.assertIn('weather', payload)
        self.assertIn('alarms', payload)
        self.assertIn('calendar', payload)

    def test_animation_endpoint_accepts_supported_actions(self):
        app = create_app(Settings(debug=True))
        client = TestClient(app)

        response = client.post('/api/animation', data={'action': 'left-ear'})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['action'], 'left-ear')
        self.assertFalse(payload['implemented'])


if __name__ == "__main__":
    unittest.main()
