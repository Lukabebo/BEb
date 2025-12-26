from __future__ import annotations

from dataclasses import dataclass, field
from random import Random
from typing import Iterable, Set, Tuple

Position = Tuple[int, int]


@dataclass
class World:
    """Grid-based world that holds item and hazard locations."""

    width: int = 6
    height: int = 6
    artifacts: Set[Position] = field(default_factory=set)
    hazards: Set[Position] = field(default_factory=set)
    exit_position: Position = (5, 5)
    seed: int | None = None

    def __post_init__(self) -> None:
        rng = Random(self.seed)
        if not self.artifacts:
            self.artifacts = self._scatter(rng, count=4, banned={self.exit_position, (0, 0)})
        if not self.hazards:
            banned = {self.exit_position, (0, 0)} | self.artifacts
            self.hazards = self._scatter(rng, count=3, banned=banned)

    def _scatter(self, rng: Random, *, count: int, banned: Iterable[Position]) -> Set[Position]:
        positions: Set[Position] = set()
        banned_set = set(banned)
        while len(positions) < count:
            pos = (rng.randrange(self.width), rng.randrange(self.height))
            if pos in banned_set or pos in positions:
                continue
            positions.add(pos)
        return positions

    def in_bounds(self, position: Position) -> bool:
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height

    def describe_tile(self, position: Position) -> str:
        if position == self.exit_position:
            return "the shimmering exit gate"
        if position in self.artifacts:
            return "a strange artifact pulsing with light"
        if position in self.hazards:
            return "a lurking hazard! You feel the cold breath of a shade"
        return "quiet stone passages"
