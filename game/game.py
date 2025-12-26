from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Tuple

from .player import Player
from .world import Position, World

DIRECTIONS: Dict[str, Position] = {
    "n": (0, -1),
    "s": (0, 1),
    "e": (1, 0),
    "w": (-1, 0),
}


@dataclass
class Game:
    """Encapsulates the turn-based adventure."""

    world: World = field(default_factory=World)
    player: Player = field(default_factory=Player)
    log: list[str] = field(default_factory=list)
    visited: set[Position] = field(default_factory=lambda: {(0, 0)})

    def _apply_move(self, direction: str) -> bool:
        delta = DIRECTIONS[direction]
        new_position = tuple(map(sum, zip(self.player.position, delta)))
        if not self.world.in_bounds(new_position):
            self.log.append("You bump into a cavern wall.")
            return False
        self.player.move(delta)
        self.visited.add(self.player.position)
        return True

    def _resolve_tile(self) -> None:
        position = self.player.position
        description = self.world.describe_tile(position)
        self.log.append(f"You reach {description}.")

        if position in self.world.artifacts:
            self.player.collect(position)
            self.world.artifacts.remove(position)
            self.log.append("You scoop up the artifact. Power thrums in your pack!")

        if position in self.world.hazards:
            self.player.hurt()
            self.log.append("A shade lashes out. Your heart pounds (health -1).")
            self.world.hazards.remove(position)

    def available_actions(self) -> Iterable[str]:
        actions = ["n", "s", "e", "w", "rest", "map", "help", "quit"]
        return actions

    def step(self, action: str) -> str:
        action = action.lower().strip()
        if action in DIRECTIONS:
            moved = self._apply_move(action)
            if moved:
                self._resolve_tile()
        elif action == "rest":
            self.log.append("You listen to the dripping stone. Nothing moves.")
        elif action == "map":
            return self.render_map()
        elif action == "help":
            return self.help_text()
        elif action == "quit":
            return "quit"
        else:
            self.log.append("That action echoes into darkness. Try n/s/e/w/rest/map/help/quit.")
        return self.status()

    def status(self) -> str:
        health_bar = "♥" * self.player.health + "·" * (3 - self.player.health)
        summary = (
            f"Health: {health_bar}   Score: {self.player.score}   "
            f"Artifacts remaining: {len(self.world.artifacts)}"
        )
        recent = "\n".join(self.log[-3:])
        return f"{summary}\n{recent}"

    def render_map(self) -> str:
        tiles: list[list[str]] = [["·" for _ in range(self.world.width)] for _ in range(self.world.height)]
        for x, y in self.visited:
            tiles[y][x] = " "+"·"+" "
        px, py = self.player.position
        tiles[py][px] = "[P]"
        ex, ey = self.world.exit_position
        tiles[ey][ex] = " < >"
        lines = ["".join(row) for row in tiles]
        return "Map legend: [P]=you, < >=exit, dots=explored\n" + "\n".join(lines)

    def help_text(self) -> str:
        return (
            "Commands: n/s/e/w to move, rest to hold still, map to view explored space, "
            "quit to leave, help to see this text. Find artifacts and reach the exit."
        )

    def is_won(self) -> bool:
        return self.player.position == self.world.exit_position and self.player.score >= 2

    def is_lost(self) -> bool:
        return self.player.health <= 0

    def intro(self) -> str:
        return (
            "You descend into the Starlit Caverns. Gather artifacts to fuel the exit gate. "
            "At least two are needed to activate it. Beware the shades that stalk the dark."
        )
