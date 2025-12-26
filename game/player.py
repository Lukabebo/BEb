from __future__ import annotations

from dataclasses import dataclass, field
from typing import Set, Tuple

Position = Tuple[int, int]


@dataclass
class Player:
    """Player state for the adventure."""

    position: Position = (0, 0)
    health: int = 3
    artifacts_collected: Set[Position] = field(default_factory=set)
    score: int = 0

    def move(self, delta: Position) -> None:
        dx, dy = delta
        x, y = self.position
        self.position = (x + dx, y + dy)

    def collect(self, position: Position) -> None:
        if position not in self.artifacts_collected:
            self.artifacts_collected.add(position)
            self.score += 1

    def hurt(self) -> None:
        self.health -= 1
