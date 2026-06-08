import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine
from app.models import Base, Game

GAMES = [
    {"title": "Hollow Knight", "genre": "metroidvania", "platform": "PC", "release_year": 2017, "cover_url": "https://example.com/hollow-knight.jpg"},
    {"title": "Elden Ring", "genre": "action-rpg", "platform": "PS5", "release_year": 2022, "cover_url": "https://example.com/elden-ring.jpg"},
    {"title": "Stardew Valley", "genre": "farming-sim", "platform": "PC", "release_year": 2016, "cover_url": "https://example.com/stardew.jpg"},
    {"title": "Celeste", "genre": "platformer", "platform": "Nintendo Switch", "release_year": 2018, "cover_url": "https://example.com/celeste.jpg"},
    {"title": "Hades", "genre": "roguelike", "platform": "PC", "release_year": 2020, "cover_url": "https://example.com/hades.jpg"},
]

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    imported = 0
    for data in GAMES:
        existing = db.query(Game).filter(Game.title == data["title"]).first()
        if existing:
            continue
        game = Game(
            title=data["title"],
            genre=data["genre"],
            platform=data["platform"],
            release_year=data["release_year"],
            cover_url=data["cover_url"],
        )
        db.add(game)
        imported += 1

    db.commit()
    db.close()
    print(f"Imported {imported} games.")

if __name__ == "__main__":
    run()
