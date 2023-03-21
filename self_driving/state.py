from dataclasses import dataclass
import numpy as np

SAMPLE_TIME = 0.05

@dataclass
class State:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    left_speed: int = 0
    right_speed: int = 0
    stopped: bool = False

    @property
    def theta(self):
        return np.arctan2(self.x, self.z)

    def __str__(self):
        # Make sure to print to 2 decimal places
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f}, {self.theta:.2f}) \t-> ({self.left_speed}, {self.right_speed})"