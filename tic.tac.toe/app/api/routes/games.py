from datetime import datetime, timezone
import uuid

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.game import Game
from app.models.user import User
from app.schemas.game import GameOut
from app.services import tictactoe

router = APIRouter()


async def _get_game(db: AsyncSession, game_id: uuid.UUID) -> Game | None:
    result = await db.execute(select(Game).where(Game.id == game_id))
    return result.scalar_one_or_none()


async def _get_game_for_user(
    db: AsyncSession, game_id: uuid.UUID, user_id: uuid.UUID
) -> Game | None:
    result = await db.execute(
        select(Game).where(
            Game.id == game_id,
            or_(Game.player_x_id == user_id, Game.player_o_id == user_id),
        )
    )
    return result.scalar_one_or_none()


@router.post("", response_model=GameOut, status_code=status.HTTP_201_CREATED)
async def create_game(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Game:
    game = Game(player_x_id=current_user.id)
    db.add(game)
    await db.commit()
    await db.refresh(game)
    return game


@router.post("/{game_id}/join", response_model=GameOut)
async def join_game(
    game_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Game:
    game = await _get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    if game.player_x_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Owner already joined")
    if game.player_o_id is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Game already has O player")
    if game.status != "IN_PROGRESS":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Game already finished")

    game.player_o_id = current_user.id
    await db.commit()
    await db.refresh(game)
    return game


@router.get("", response_model=list[GameOut])
async def list_games(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[Game]:
    result = await db.execute(
        select(Game)
        .where(or_(Game.player_x_id == current_user.id, Game.player_o_id == current_user.id))
        .order_by(Game.created_at.desc())
    )
    return list(result.scalars().all())


@router.get("/{game_id}", response_model=GameOut)
async def get_game(
    game_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Game:
    game = await _get_game_for_user(db, game_id, current_user.id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    return game


@router.put("/{game_id}/move/{position}", response_model=GameOut)
async def make_move(
    game_id: uuid.UUID,
    position: int = Path(..., ge=1, le=9),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Game:
    game = await _get_game_for_user(db, game_id, current_user.id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    if game.status != "IN_PROGRESS":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Game already finished")

    if game.next_player == "X":
        if current_user.id != game.player_x_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Not your turn")
    else:
        if game.player_o_id is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Waiting for opponent")
        if current_user.id != game.player_o_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Not your turn")

    index = position - 1
    if game.board[index] != ".":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Position already taken")

    current_player = game.next_player
    game.board = tictactoe.apply_move(game.board, position, current_player)
    game.moves.append(
        {
            "player": current_player,
            "position": position,
            "at": datetime.now(timezone.utc).isoformat(),
        }
    )
    game.status = tictactoe.compute_status(game.board)
    if game.status == "IN_PROGRESS":
        game.next_player = tictactoe.toggle_player(current_player)

    await db.commit()
    await db.refresh(game)
    return game

@router.get("/{game_id}/export", response_class=Response)
async def export_game_xml(
    game_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Response:
    import xml.etree.ElementTree as ET
 
    game = await _get_game_for_user(db, game_id, current_user.id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
 
    root = ET.Element("game", id=str(game.id))
 
    ET.SubElement(root, "status").text = game.status
    ET.SubElement(root, "next_player").text = game.next_player
    ET.SubElement(root, "board").text = game.board
    ET.SubElement(root, "created_at").text = game.created_at.isoformat()
    ET.SubElement(root, "updated_at").text = game.updated_at.isoformat()
 
    players_el = ET.SubElement(root, "players")
    ET.SubElement(players_el, "player_x_id").text = str(game.player_x_id)
    ET.SubElement(players_el, "player_o_id").text = str(game.player_o_id) if game.player_o_id else ""
 
    moves_el = ET.SubElement(root, "moves")
    for m in game.moves:
        move_el = ET.SubElement(moves_el, "move")
        ET.SubElement(move_el, "player").text = m["player"]
        ET.SubElement(move_el, "position").text = str(m["position"])
        ET.SubElement(move_el, "at").text = m["at"]
 
    xml_bytes = ET.tostring(root, encoding="utf-8", xml_declaration=True)
 
    return Response(
        content=xml_bytes,
        media_type="application/xml",
        headers={
            "Content-Disposition": f'attachment; filename="game_{game_id}.xml"'
        },
    )

@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(
    game_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Response:
    game = await _get_game_for_user(db, game_id, current_user.id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    if game.status == "IN_PROGRESS":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Game still in progress")

    await db.delete(game)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
