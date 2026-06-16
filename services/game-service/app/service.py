# Application layer — business logic.
#
# Calls repository functions and returns Pydantic schemas (not raw ORM objects).
# Raises ValueError when a game is not found — routes.py turns it into a 404.
#
# Implement these four functions:
# - add_game(db, data) -> GameOut
# - fetch_game(db, game_id) -> GameOut        (raises ValueError if not found)
# - fetch_all_games(db, limit, offset) -> GameList
# - find_games(db, q, limit, offset) -> GameList   (delegates to search_games in repository)
#
# Module 5 — CQRS:
# In add_game(), after saving to the DB, also write to the Redis cache:
#   from app.infrastructure.cache import set_game_summary
#   set_game_summary(game.id, {"id": game.id, "title": game.title,
#                               "genre": game.genre, "platform": game.platform,
#                               "cover_url": game.cover_url})
from sqlalchemy.orm import Session

from app.infrastructure.cache import set_game_summary
import app.repository as repo
from app.schemas import GameCreate, GameList, GameResponse


def add_game(db: Session, data: GameCreate) -> GameResponse:
    game = repo.create_game(db, data)
    set_game_summary(game.id, {
        "id": game.id,
        "title": game.title,
        "genre": game.genre,
        "platform": game.platform,
        "cover_url": game.cover_url,
    })
    return GameResponse.model_validate(game)


def get_game(db: Session, game_id: str) -> GameResponse | None:
    game = repo.get_game(db, game_id)
    if game is None:
        return None
    return GameResponse.model_validate(game)


def list_games(db: Session, limit: int = 20, offset: int = 0) -> GameList:
    games, total = repo.list_games(db, limit=limit, offset=offset)
    return GameList(
        items=[GameResponse.model_validate(g) for g in games],
        total=total,
        limit=limit,
        offset=offset,
    )


def search_games(db: Session, q: str) -> GameList:
    games, total = repo.search_games(db, q)
    return GameList(
        items=[GameResponse.model_validate(g) for g in games],
        total=total,
        limit=20,
        offset=0,
    )


def remove_game(db: Session, game_id: str) -> bool:
    return repo.delete_game(db, game_id)
