import chess
import random

PAWN_VALUE = 1
KNIGHT_VALUE = 3
BISHOP_VALUE = 3
ROOK_VALUE = 5
QUEEN_VALUE = 9


class Player:
    colour: chess.Color

    def __init__(self, colour: chess.Color) -> None:
        self.colour = colour

    def evaluate_position(self, board: chess.Board) -> float:
        score = 0
        # First evaluate the material balance. Our own pieces have a positive value
        # and the opponent's pieces have a negative value. Don't count the kings as they can
        # never leave the board.
        score += (
            len(board.pieces(chess.PAWN, self.colour)) * PAWN_VALUE
            - len(board.pieces(chess.PAWN, not (self.colour))) * PAWN_VALUE
        )
        score += (
            len(board.pieces(chess.KNIGHT, self.colour)) * KNIGHT_VALUE
            - len(board.pieces(chess.KNIGHT, not (self.colour))) * KNIGHT_VALUE
        )
        score += (
            len(board.pieces(chess.BISHOP, self.colour)) * BISHOP_VALUE
            - len(board.pieces(chess.BISHOP, not (self.colour))) * BISHOP_VALUE
        )
        score += (
            len(board.pieces(chess.ROOK, self.colour)) * ROOK_VALUE
            - len(board.pieces(chess.ROOK, not (self.colour))) * ROOK_VALUE
        )
        score += (
            len(board.pieces(chess.QUEEN, self.colour)) * QUEEN_VALUE
            - len(board.pieces(chess.QUEEN, not (self.colour))) * QUEEN_VALUE
        )
        return score

    def get_move(self, board: chess.Board) -> chess.Move:
        # Make a copy of the board for analysis
        # so we do not mutate the original.
        next_move: chess.Move = None
        next_move_score = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            candidate_move_score = self.evaluate_position(board)
            if candidate_move_score > next_move_score:
                next_move = move
                next_move_score = candidate_move_score
            board.pop()
        return next_move
