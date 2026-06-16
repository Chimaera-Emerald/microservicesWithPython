# Application layer — Pydantic DTOs.
#
# Define the shapes of data coming IN and going OUT of the API.
#
# This file should define:
# - GameCreate  — fields accepted when creating a game
#                 (title, genre, platform required; release_year and cover_url optional)
# - GameOut     — fields returned to the caller (includes id and created_at)
#                 add model_config = {"from_attributes": True}
# - GameList    — paginated envelope: { items, total, limit, offset }
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class GameCreate(BaseModel):
    title: str
    genre: str
    platform: str
    release_year: Optional[int] = None
    cover_url: Optional[str] = None


class GameResponse(BaseModel):
    id: str
    title: str
    genre: str
    platform: str
    release_year: Optional[int] = None
    cover_url: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class GameList(BaseModel):
    items: List[GameResponse]
    total: int
    limit: int
    offset: int
