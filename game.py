from __future__ import annotations
import chess
from player import Player


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

    def make_move_if_legal(self: Game, move: chess.Move) -> bool:
        if move in list(self.board.legal_moves):
            self.board.push(move)
            return True
        else:
            print("Illegal move")
            return False


def new_game() -> Game:
    print("Starting a new game")
    print("Starting position")
    game = Game()
    print(game.board)
    return game


def play_game() -> None:
    game = new_game()
    black_player = Player(chess.BLACK)
    while not game.game_over():
        while True:
            if game.board.turn == chess.WHITE:
                print(game.board.legal_moves)
                print("Enter move for white:")
                move = str(input())
                try:
                    print("attempting to parse white move")
                    move = game.board.parse_san(move)
                except:
                    if move == "resign":
                        break
                    else:
                        print(
                            "Unable to parse move. Please use valid SAN notiation or type 'resign' to resign."
                        )
                        continue
            else:
                move = black_player.get_move(game.board)
                print(f"Black's move: {move}")
            if game.make_move_if_legal(move):
                break
        if move == "resign":
            print(
                f"{'white' if game.board.turn == chess.WHITE else 'black'} resigns. Game over."
            )
            break
        print(game.board)
