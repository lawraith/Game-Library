import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI(title="Game Library API")

FILE_PATH = Path(__file__).parent / "games.json"   


class GameCreate(BaseModel):
    name: str
    genre: str


class GameUpdate(BaseModel):
    name: str | None = None
    genre: str | None = None


def load_games():
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_games(games):
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(games, file, ensure_ascii=False, indent=4)


@app.get("/")
def home():
    return {"message": "Welcome to Game Library API"}


@app.get("/health")
def health_check():
    return {"status": "OK"}


@app.get("/games")
def get_games():
    return load_games()


@app.get("/games")
def get_games(
    search: str | None = None,
    genre: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    games = load_games()

    if search:
        games = [
            game for game in games
            if search.lower() in game["name"].lower()
        ]

    if genre:
        games = [
            game for game in games
            if game["genre"].lower() == genre.lower()
        ]

    return games[offset:offset + limit]


@app.post("/games", status_code=201)
def add_game(game_data: GameCreate):
    games = load_games()

    for game in games:
        if game["name"].lower() == game_data.name.lower():
            raise HTTPException(status_code=409, detail="Game already exists")

    new_game = {
        "id": max((game["id"] for game in games), default=0) + 1,
        "name": game_data.name,
        "genre": game_data.genre
    }

    games.append(new_game)
    save_games(games)

    return new_game


@app.patch("/games/{game_id}")
def update_game(game_id: int, game_data: GameUpdate):
    games = load_games()

    for game in games:
        if game["id"] == game_id:
            updates = game_data.model_dump(exclude_unset=True)

            game.update(updates)
            save_games(games)

            return game

    raise HTTPException(status_code=404, detail="Game not found")


@app.delete("/games/{game_id}")
def delete_game(game_id: int):
    games = load_games()

    for game in games:
        if game["id"] == game_id:  
            games.remove(game)
            save_games(games)
            return {"message": "Game deleted successfully"}

    raise HTTPException(status_code=404, detail="Game not found")