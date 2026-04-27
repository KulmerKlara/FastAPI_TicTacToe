import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.game import Game


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(engine)


def test_game_initialization():
    game = Game(
        player_x_id=uuid.uuid4(),
        player_o_id=None,
        board=".........",
        moves=[],
        status="IN_PROGRESS",
        next_player="X",
    )

    assert game.board == "........."
    assert game.moves == []
    assert game.status == "IN_PROGRESS"
    assert game.next_player == "X"


def test_game_constraints(session):
    game = Game(
        player_x_id=uuid.uuid4(),
    )

    session.add(game)
    session.commit()

    db_game = session.query(Game).first()

    assert db_game is not None
    assert db_game.board == "........."
    assert db_game.status == "IN_PROGRESS"
    assert db_game.next_player == "X"