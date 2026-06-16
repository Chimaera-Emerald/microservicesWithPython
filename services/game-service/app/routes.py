from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.infrastructure.cache import get_game_summary
from app.schemas import GameCreate, GameList, GameResponse
from app.security import require_admin
from app.service import add_game, get_game, list_games, remove_game, search_games

router = APIRouter(prefix="/v1/games")


@router.post("/", response_model=GameResponse, status_code=201)
def create_game(data: GameCreate, db: Session = Depends(get_db)):
    return add_game(db, data)


@router.get("/", response_model=GameList)
def list_games_endpoint(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    return list_games(db, limit=limit, offset=offset)


@router.get("/search", response_model=GameList)
def search_games_endpoint(q: str = "", db: Session = Depends(get_db)):
    return search_games(db, q)


@router.get("/{game_id}/summary")
def game_summary(game_id: str):
    data = get_game_summary(game_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Summary not cached")
    return data


@router.get("/{game_id}", response_model=GameResponse)
def get_game_endpoint(game_id: str, db: Session = Depends(get_db)):
    game = get_game(db, game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.delete("/{game_id}", dependencies=[Depends(require_admin)])
def delete_game_endpoint(game_id: str, db: Session = Depends(get_db)):
    deleted = remove_game(db, game_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"deleted": True}
