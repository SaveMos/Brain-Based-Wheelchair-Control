import uuid
import random
from typing import List

from segregation_system.prepared_session import PreparedSession


def generate_random_prepared_sessions_object(n : int) -> List[PreparedSession]:
    randomized_prepared_sessions = [
        PreparedSession(
            uuid=str(uuid.uuid4()),  # Random UUID for each session
            features=[
                random.uniform(0.1, 1.0),  # Random feature values
                random.uniform(0.1, 1.0),  # Random feature values
                random.uniform(0.1, 1.0),  # Random feature values
                random.uniform(0.1, 1.0),  # Random feature values
                random.choice(["gaming", "shopping", "sport", "relax"]),
                random.choice(["plain", "slippery", "slope", "house", "track"]),
            ],
            label=random.choice(["move", "turn_left", "turn_right"])  # Random label
        )
        for _ in range(n)
    ]
    return randomized_prepared_sessions