import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi.testclient import TestClient

from nabazhome_luckfox.api.app import create_app
from nabazhome_luckfox.config.settings import Settings
from nabazhome_luckfox.domain.alarm import AlarmSchedule


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

    def test_alarm_can_ring_and_be_disabled(self):
        db_path = Path(tempfile.mkdtemp()) / 'dashboard-alarm.db'
        app = create_app(Settings(db_path=db_path, debug=True))
        client = TestClient(app)

        app.state.alarm_service.current_alarm = AlarmSchedule(
            id='alarm-due-now',
            name='Wake-up',
            trigger_at=datetime.now() - timedelta(minutes=1),
            enabled=True,
            recurring=True,
        )

        dashboard_response = client.get('/api/dashboard')
        self.assertTrue(dashboard_response.json()['ringing'])
        self.assertEqual(dashboard_response.json()['device']['status'], 'alerting')
        self.assertEqual(len(dashboard_response.json()['alarms']), 1)

        disable_response = client.post('/alarms/disable')
        self.assertEqual(disable_response.status_code, 200)

        persisted_response = client.get('/api/dashboard')
        self.assertFalse(persisted_response.json()['ringing'])
        self.assertEqual(persisted_response.json()['device']['status'], 'ready')
        self.assertEqual(len(persisted_response.json()['alarms']), 0)

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
