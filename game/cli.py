from __future__ import annotations

from .game import Game


def run() -> None:
    game = Game()
    print(game.intro())
    print(game.status())

    while True:
        action = input("Action (n/s/e/w/rest/map/help/quit): ")
        result = game.step(action)

        if result == "quit":
            print("You leave the caverns behind. Farewell.")
            break

        print(result)

        if game.is_won():
            print("The exit gate hums to life! You escape with your prizes. You win!")
            break
        if game.is_lost():
            print("The shades overwhelm you. Darkness closes in. Game over.")
            break


if __name__ == "__main__":
    run()
