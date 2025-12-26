import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from game.game import Game
from game.world import World


def test_world_generation_reproducible():
    world_one = World(seed=42)
    world_two = World(seed=42)
    assert world_one.artifacts == world_two.artifacts
    assert world_one.hazards == world_two.hazards


def test_game_winning_path_without_hazards():
    world = World(
        artifacts={(2, 0), (4, 0), (2, 2)},
        hazards=set(),
        exit_position=(5, 5),
    )
    game = Game(world=world)

    path = ["e", "e", "e", "e", "e", "s", "s", "s", "s", "s"]
    for action in path:
        game.step(action)
        if game.is_won() or game.is_lost():
            break

    assert game.player.score >= 2
    assert game.is_won()
