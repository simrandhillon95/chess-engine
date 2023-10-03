import chess

PIECES = [
    (chess.PAWN, 1),
    (chess.KNIGHT, 3),
    (chess.BISHOP, 3),
    (chess.ROOK, 5),
    (chess.QUEEN, 9),
]


class Player:
    colour: chess.Color

    def __init__(self, colour: chess.Color) -> None:
        self.colour = colour

    def move_is_legal(board: chess.Board, move: chess.Move) -> bool:
        if move in list(board.legal_moves):
            return True
        else:
            print("Illegal move. Please supply a legal move.")
            return False


class HumanPlayer(Player):
    def get_move(self, board: chess.Board) -> chess.Move:
        print(board.legal_moves)
        print(f"Enter move for {'white' if self.colour == chess.WHITE else 'black'}:")
        while True:
            move = str(input())
            try:
                print(f"Attempting to parse move: {move}")
                move = board.parse_san(move)
                return move
            except:
                if move == "resign":
                    break
                else:
                    print(
                        "Unable to parse move. Please use valid SAN notation or type 'resign' to resign."
                    )
                    continue


class EnginePlayer(Player):
    search_depth: int = 1

    def evaluate_position(self, board: chess.Board) -> float:
        score = 0
        # First evaluate the material balance. The engine's pieces have a positive value
        # and the opponent's pieces have a negative value. Don't count the kings as they can
        # never leave the board.
        for piece, value in PIECES:
            score += (
                len(board.pieces(piece, self.colour)) * value
                - len(board.pieces(piece, not (self.colour))) * value
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
