import uuid
from datetime import datetime

import pytest

from app.schemas.game import GameOut, Move, Player, GameStatus


def test_move_validation():
    move = Move(
        player=Player.X,
        position=5,
        at=datetime.utcnow()
    )

    assert move.player == Player.X
    assert 1 <= move.position <= 9


def test_game_out_creation():
    game = GameOut(
        id=uuid.uuid4(),
        player_x_id=uuid.uuid4(),
        player_o_id=None,
        board=".........",
        moves=[
            Move(
                player=Player.X,
                position=1,
                at=datetime.utcnow()
            )
        ],
        status=GameStatus.IN_PROGRESS,
        next_player=Player.O,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    assert game.status == GameStatus.IN_PROGRESS
    assert game.board == "........."
    assert len(game.moves) == 1
    assert game.moves[0].player == Player.X


def test_position_validation_error():
    with pytest.raises(ValueError):
        Move(
            player=Player.X,
            position=99,
            at=datetime.utcnow()
        )