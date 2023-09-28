from chess import Board
import random


class Player:
    def get_move(self, board: Board) -> str:
        move = random.choice(list(board.legal_moves))
        return move.uci()
