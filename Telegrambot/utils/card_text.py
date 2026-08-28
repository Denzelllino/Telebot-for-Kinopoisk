

def card_text(item):
    title = item.get("title") or item.get("name") or "Без названия"
    desc = item.get("description") or item.get("shortDescription") or item.get("overview") or "Нет описания"
    rating = item.get("rating")
    if isinstance(rating, dict):
        rating = rating.get("kp", "-")
    rating = rating if rating is not None else "-"
    year = item.get("year") or "-"
    genres = ", ".join(g.get("name", "") for g in item.get("genres", []) if g.get("name")) or "-"
    age = item.get("ageRating") or item.get("ratingMpaa") or "-"
    poster = item.get("poster")
    if isinstance(poster, dict):
        poster = poster.get("url") or "-"
    poster = poster or "-"
    return (
        f"Название: {title}\n"
        f"Описание: {desc}\n"
        f"Рейтинг: {rating}\n"
        f"Год производства: {year}\n"
        f"Жанр: {genres}\n"
        f"Возрастной рейтинг: {age}\n"
        f"Постер: {poster}"
    )