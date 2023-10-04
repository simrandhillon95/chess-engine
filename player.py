import chess
from time import time_ns

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
    _nodes_searched = 0

    def evaluate_position(self, board: chess.Board) -> float:
        # The evaluation of a position is the sum of many considerations.
        # The nature and accuracy of these considerations determine both how
        # expensive the computation is and how well the engine will play. It
        # is important to be efficient.
        # The calculations here are inlined to avoid the overhead of additional
        # function calls.
        score = 0
        ####################
        # Material balance #
        ####################
        for piece, value in PIECES:
            score += (
                len(board.pieces(piece, self.colour)) * value
                - len(board.pieces(piece, not (self.colour))) * value
            )
        ############
        # Mobility #
        ############
        legal_moves = board.legal_moves.count()
        if legal_moves > 0:
            mobility_score = legal_moves * 0.1
            if board.turn == self.colour:
                score += mobility_score
            else:
                score -= mobility_score
        #####################
        # Checkmate threats #
        #####################
        elif board.is_checkmate():
            score += 1000 if board.turn == self.colour else -1000
        return score

    def search(
        self,
        board: chess.Board,
        depth: int,
        alpha: float,
        beta: float,
        search_depth: int,
        move_list: list,
    ) -> (chess.Move, int):
        # If we have not reached the maximum depth and there are still
        # legal moves to evaluate, carry on recursing.
        if depth < search_depth and board.legal_moves.count() != 0:
            # Initialise the best move to have a value of -inf or +inf,
            # depending on whether we are maximising or minimising. This
            # guarantees that it will be replaced by an actual candidate move.
            if board.turn == self.colour:
                # Engine's turn
                best_move = (None, float("-inf"))
            else:
                # Opponent's turn
                best_move = (None, float("+inf"))
            for current_candidate in (
                board.legal_moves if move_list is None else move_list
            ):
                # Play the move so we can search the resulting position.
                board.push(current_candidate)
                _, value = self.search(
                    board, depth + 1, alpha, beta, search_depth, None
                )
                board.pop()
                # If it is the engine's turn, find the move which
                # maximises the evaluation.
                if board.turn == self.colour:
                    if value > best_move[1]:
                        best_move = (current_candidate, value)
                    # We are maximising, so replace alpha if we have
                    # found a better move.
                    alpha = max(alpha, best_move[1])
                # If it is the opponents turn, find the move which
                # minimises the evaluation.
                elif board.turn != self.colour:
                    if value < best_move[1]:
                        best_move = (current_candidate, value)
                    # We are minimising, so replace beta if we
                    # have found a better (for the minimising player) move.
                    beta = min(beta, best_move[1])
                # This means the branch is guaranteed to yield a better result for the minimiser (opponent)
                # than the maximiser could guarantee elsewhere. There is no need to continue searching.
                if beta <= alpha:
                    break
            return best_move
        # We have reached the maximum depth or a leaf of the tree. Here we need to end recursion
        # and return the last move played and the evaluation of the resulting position.
        else:
            self._nodes_searched += 1
            return (None, self.evaluate_position(board))

    def get_move(self, board: chess.Board) -> chess.Move:
        # Make a copy of the board for analysis
        # so we do not mutate the original.
        self._nodes_searched = 0
        move_list = list(board.legal_moves)
        start_time = time_ns()
        for iter_depth in range(self.search_depth):
            next_move, _ = self.search(
                board,
                depth=0,
                alpha=float("-inf"),
                beta=float("+inf"),
                search_depth=iter_depth + 1,
                move_list=move_list,
            )
            # To see the benefit of iterative deepening, the best move
            # from each iteration should be the first move searched in
            # the next iteration.
            if move_list[0] != next_move:
                move_list.remove(next_move)
                move_list.insert(0, next_move)
        end_time = time_ns()
        print(
            f"Searched {self._nodes_searched} nodes in {(end_time - start_time)/10**6} ms"
        )
        return next_move
