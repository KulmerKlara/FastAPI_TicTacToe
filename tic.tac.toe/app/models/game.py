import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Game(Base):
    __tablename__ = "games"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_x_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    player_o_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    board: Mapped[str] = mapped_column(String(9), nullable=False, default=".........")
    moves: Mapped[list] = mapped_column(MutableList.as_mutable(JSON), default=list, nullable=False)
    status: Mapped[str] = mapped_column(String(12), nullable=False, default="IN_PROGRESS")
    next_player: Mapped[str] = mapped_column(String(1), nullable=False, default="X")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    player_x = relationship("User", foreign_keys=[player_x_id], back_populates="games_x")
    player_o = relationship("User", foreign_keys=[player_o_id], back_populates="games_o")
