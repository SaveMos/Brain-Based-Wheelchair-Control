import random
import uuid
from unittest import TestCase

from segregation_system.balancing_report import BalancingReport
from segregation_system.prepared_session import PreparedSession


class TestBalancingReport(TestCase):
    def setUp(self):
        self.prepared_sessions = [
            PreparedSession(
                uuid=str(uuid.uuid4()),  # Random UUID for each session
                features=[
                    random.uniform(0.1, 1.0), # Random feature values
                    random.uniform(0.1, 1.0), # Random feature values
                    random.uniform(0.1, 1.0), # Random feature values
                    random.uniform(0.1, 1.0), # Random feature values
                    random.choice(["gaming", "shopping", "sport", "relax"]),
                    random.choice(["plain", "slippery", "slope", "house", "track"]),
                ],
                label=random.choice(["move", "turn_left", "turn_right"])  # Random label
            )
            for _ in range(20)
        ]

    def test_balancing_report(self):
        # Create BalancingReport from prepared sessions
        bal = BalancingReport(self.prepared_sessions)

        # Count labels manually
        expected_counts = {"move": 0, "turn_left": 0, "turn_right": 0}
        for session in self.prepared_sessions:
            expected_counts[session.label] += 1

        # Verify that the counts match the expected values
        self.assertEqual(bal.move, expected_counts["move"], "The count for 'move' is incorrect.")
        self.assertEqual(bal.turn_left, expected_counts["turn_left"], "The count for 'turn_left' is incorrect.")
        self.assertEqual(bal.turn_right, expected_counts["turn_right"], "The count for 'turn_right' is incorrect.")

        print("Test passed. Balancing report matches expected values.")
