from typing import Optional


WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def apply_move(board: str, position: int, player: str) -> str:
    index = position - 1
    board_list = list(board)
    board_list[index] = player
    return "".join(board_list)


def check_winner(board: str) -> Optional[str]:
    for a, b, c in WINNING_LINES:
        if board[a] != "." and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_draw(board: str) -> bool:
    return "." not in board and check_winner(board) is None


def compute_status(board: str) -> str:
    winner = check_winner(board)
    if winner == "X":
        return "X_WON"
    if winner == "O":
        return "O_WON"
    if is_draw(board):
        return "DRAW"
    return "IN_PROGRESS"


def toggle_player(player: str) -> str:
    return "O" if player == "X" else "X"
