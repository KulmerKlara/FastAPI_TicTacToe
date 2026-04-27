from app.services.tictactoe import (apply_move, check_winner, is_draw, compute_status, toggle_player,)

# game-logic testen
def test_apply_move():
    board = "........."
    new_board = apply_move(board, 5, "X")

    assert new_board[4] == "X"
    assert len(new_board) == 9


def test_check_winner_row():
    board = "XXX......"
    assert check_winner(board) == "X"


def test_check_winner_column():
    board = "X..X..X.."
    assert check_winner(board) == "X"


def test_check_winner_diagonal():
    board = "X...X...X"
    assert check_winner(board) == "X"


def test_check_winner_none():
    board = "XOXOXO..."
    assert check_winner(board) is None


def test_is_draw_true():
    board = "XOXOXOOXO"
    assert is_draw(board) is True


def test_is_draw_false():
    board = "XOXOXO..."
    assert is_draw(board) is False


def test_compute_status_x_won():
    board = "XXX......"
    assert compute_status(board) == "X_WON"


def test_compute_status_o_won():
    board = "OOO......"
    assert compute_status(board) == "O_WON"


def test_compute_status_draw():
    board = "XOXOXOOXO"
    assert compute_status(board) == "DRAW"


def test_compute_status_in_progress():
    board = "XOX......"
    assert compute_status(board) == "IN_PROGRESS"


def test_toggle_player():
    assert toggle_player("X") == "O"
    assert toggle_player("O") == "X"