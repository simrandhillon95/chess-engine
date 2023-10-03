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
                break
            except:
                if move == "resign":
                    break
                else:
                    print(
                        "Unable to parse move. Please use valid SAN notation or type 'resign' to resign."
                    )
                    continue
        return move


class EnginePlayer(Player):
    search_depth: int = 1

    def evaluate_position(self, board: chess.Board) -> float:
        score = 0
        # First evaluate the material balance. The engine's pieces have a positive value
        # and the opponents pieces have a negative value. This means that a positive evaluation favours the
        # engine and a negative evaluation favours the opponent.
        # Don't count the kings as they can never leave the board.
        for piece, value in PIECES:
            score += (
                len(board.pieces(piece, self.colour)) * value
                - len(board.pieces(piece, not (self.colour))) * value
            )
        return score

    def search(self, board: chess.Board, depth: int) -> (chess.Move, int):
        # If we have not reached the maximum depth and there are still
        # legal moves to evaluate, carry on recursing.
        if depth < self.search_depth and board.legal_moves.count() != 0:
            # Initialise the best move to have a value of -inf or +inf,
            # depending on whether we are maximising or minimising. This
            # guarantees that it will be replaced by an actual candidate move.
            if board.turn == self.colour:
                # Engine's turn
                best_move = (None, float("-inf"))
            else:
                # Opponent's turn
                best_move = (None, float("+inf"))
            for current_candidate in board.legal_moves:
                # Play the move so we can search the resulting position.
                board.push(current_candidate)
                _, value = self.search(board, depth + 1)
                board.pop()
                # If it is the engine's turn, find the move which
                # maximises the evaluation.
                if board.turn == self.colour and value > best_move[1]:
                    best_move = (current_candidate, value)
                # If it is the opponents turn, find the move which
                # minimises the evaluation.
                elif board.turn != self.colour and value < best_move[1]:
                    best_move = (current_candidate, value)
            return best_move
        # We have reached the maximum depth or a leaf of the tree. Here we need to end recursion
        # and return the last move played and the evaluation of the resulting position.
        else:
            return (None, self.evaluate_position(board))

    def get_move(self, board: chess.Board) -> chess.Move:
        # Make a copy of the board for analysis
        # so we do not mutate the original.
        next_move, _ = self.search(board, depth=0)
        return next_move
