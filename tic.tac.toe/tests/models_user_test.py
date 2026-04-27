import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.user import User
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



def test_user_initialization(session):
    user = User(username="testuser")

    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.username == "testuser"
    assert isinstance(user.id, uuid.UUID)



def test_user_persistence_and_unique_constraint(session):
    user1 = User(username="alice")
    user2 = User(username="alice")

    session.add(user1)
    session.commit()

    session.add(user2)

    with pytest.raises(Exception):
        session.commit()