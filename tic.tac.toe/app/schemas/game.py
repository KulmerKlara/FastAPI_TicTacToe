from datetime import datetime
from enum import Enum
from typing import List, Optional
import uuid

from pydantic import BaseModel, ConfigDict, Field


class Player(str, Enum):
    X = "X"
    O = "O"


class GameStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    X_WON = "X_WON"
    O_WON = "O_WON"
    DRAW = "DRAW"


class Move(BaseModel):
    player: Player
    position: int = Field(..., ge=1, le=9)
    at: datetime


class GameOut(BaseModel):
    id: uuid.UUID
    player_x_id: uuid.UUID
    player_o_id: Optional[uuid.UUID]
    board: str
    moves: List[Move]
    status: GameStatus
    next_player: Player
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
