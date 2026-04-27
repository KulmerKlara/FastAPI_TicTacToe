import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)

    games_x = relationship("Game", back_populates="player_x", foreign_keys="Game.player_x_id")
    games_o = relationship("Game", back_populates="player_o", foreign_keys="Game.player_o_id")
