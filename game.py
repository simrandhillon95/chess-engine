from __future__ import annotations
import chess
from player import EnginePlayer, HumanPlayer, Player


class Game:
    board: chess.Board

    def __init__(self: Game) -> None:
        self.board = chess.Board()

    def game_over(self) -> bool:
        if self.board.outcome(claim_draw=True):
            print("Game over")
            return True
        else:
            return False


def new_game() -> Game:
    print("Starting a new game")
    print("Starting position")
    game = Game()
    print(game.board)
    return game


def select_config() -> (Player, Player):
    print("Please select the search depth for the engine")
    print("The maximum value allowed is 5")
    print("The minimum value allowed is 1")
    print("No input will default to a depth of 1:")
    while True:
        depth = input()
        try:
            depth = int(depth)
            if depth > 5 or depth < 1:
                print("Please select a number within the allowed range.")
                continue
            else:
                break
        except:
            print(
                "Invalid input detected. Please enter a number between 1 and 5 (inclusive)."
            )
    while True:
        print("Please select a colour to play as: [(W)/B]")
        player_colour = input()
        if player_colour == "" or player_colour == "W":
            white_player = HumanPlayer(chess.WHITE)
            black_player = EnginePlayer(chess.BLACK)
            black_player.search_depth = depth
            break
        elif player_colour == "B":
            white_player = EnginePlayer(chess.WHITE)
            black_player = HumanPlayer(chess.BLACK)
            white_player.search_depth = depth
            break
        else:
            print(
                "Unrecognised input. Please select either W or B. Entering nothing will default to white."
            )

    return (white_player, black_player)


def play_game() -> None:
    game = new_game()
    white_player, black_player = select_config()
    while not game.game_over():
        if game.board.turn == chess.WHITE:
            move = white_player.get_move(game.board)
            print(f"Whites's move: {move}")
        else:
            move = black_player.get_move(game.board)
            print(f"Black's move: {move}")
        if move == "resign":
            print(
                f"{'White' if game.board.turn == chess.WHITE else 'Black'} resigns. Game over."
            )
            break
        else:
            game.board.push(move)
        print(game.board)
