import os
import requests

from Telegrambot.config_data.config import KINOPOISK_API_KEY

BASE_URL = "https://api.kinopoisk.dev/v1.4"
TOKEN = os.getenv("KINOPOISK_TOKEN")

HEADERS = {
    "X-API-KEY": KINOPOISK_API_KEY,
    "Content-Type": "application/json"
}

def _get(path, params=None):
    r = requests.get(f"{BASE_URL}{path}", headers=HEADERS, params=params or {}, timeout=30)
    r.raise_for_status()
    return r.json()

def random_movie():
    return _get(f"/movie/random" + f'?notNullFields=name&notNullFields=description')

def search_movies(query, limit=10, page=1, media_type=None, genre=None):
    params = {"query": query, "limit": limit, "page": page}
    if media_type:
        params["type"] = media_type
    if genre:
        params["genres.name"] = genre
    return _get("/movie/search", params)

def get_movie(movie_id):
    return _get(f"/movie/{movie_id}")

def search_by_rating(min_rating=7, max_rating=10, genre=None, limit=10, page=1, media_type=None):
    params = {
        "limit": limit,
        "page": page,
        "rating.kp": f"{min_rating}-{max_rating}",
        "sortField": "rating.kp",
        "sortType": -1
    }
    if genre:
        params["genres.name"] = genre
    if media_type:
        params["type"] = media_type
    return _get("/movie", params)

def search_by_budget(min_budget=None, max_budget=None, genre=None, limit=10, page=1, media_type=None):
    params = {
        "limit": limit,
        "page": page,
        "sortField": "budget.value",
        "sortType": -1
    }
    if genre:
        params["genres.name"] = genre
    if media_type:
        params["type"] = media_type

    data = _get("/movie", params)
    docs = data.get("docs", [])
    filtered = []

    for item in docs:
        budget = None
        if isinstance(item.get("budget"), dict):
            budget = item["budget"].get("value")
        if budget is None:
            detail = get_movie(item["id"])
            if isinstance(detail.get("budget"), dict):
                budget = detail["budget"].get("value")
            item = detail

        if budget is None:
            continue
        if min_budget is not None and budget < min_budget:
            continue
        if max_budget is not None and budget > max_budget:
            continue
        filtered.append(item)

    data["docs"] = filtered
    return data