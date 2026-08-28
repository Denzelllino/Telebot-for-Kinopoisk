import os
from dotenv import load_dotenv
import telebot

from Telegrambot.api.kinopoisk_api import search_movies, search_by_rating, search_by_budget
from Telegrambot.database.db import init_db, save_item, get_history, set_viewed
from Telegrambot.keyboards.inline.keyboards import main_menu, pager, history_actions, content_type_kb

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
user_state = {}

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

def start_flow(message, mode):
    user_state[message.from_user.id] = {"mode": mode}
    bot.send_message(message.chat.id, "Выберите тип контента:", reply_markup=content_type_kb())

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Выберите команду:", reply_markup=main_menu())

@bot.message_handler(commands=["help"])
def help_cmd(message):
    bot.send_message(
        message.chat.id,
        "Меню:\n"
        "movie_search\nmovie_by_rating\nlow_budget_movie\nhigh_budget_movie\nhistory"
    )

@bot.callback_query_handler(func=lambda call: call.data in {
    "movie_search", "movie_by_rating", "low_budget_movie", "high_budget_movie", "history"
})
def menu_handler(call):
    bot.answer_callback_query(call.id)
    if call.data == "history":
        msg = bot.send_message(call.message.chat.id, "Введите дату в формате YYYY-MM-DD:")
        bot.register_next_step_handler(msg, history_date_handler)
        return
    start_flow(call.message, call.data)

@bot.callback_query_handler(func=lambda call: call.data.startswith("type:"))
def type_handler(call):
    bot.answer_callback_query(call.id)
    state = user_state.get(call.from_user.id)
    if not state:
        return
    state["type"] = call.data.split(":", 1)[1]
    msg = bot.send_message(call.message.chat.id, "Введите название фильма/сериала:")
    bot.register_next_step_handler(msg, ask_genre)

def ask_genre(message):
    state = user_state.setdefault(message.from_user.id, {})
    state["title"] = message.text.strip()
    msg = bot.send_message(message.chat.id, "Введите жанр (например: комедия, ужасы, фантастика):")
    bot.register_next_step_handler(msg, ask_count)

def ask_count(message):
    state = user_state.setdefault(message.from_user.id, {})
    state["genre"] = message.text.strip()
    msg = bot.send_message(message.chat.id, "Введите количество вариантов:")
    bot.register_next_step_handler(msg, process_count)

def process_count(message):
    state = user_state.setdefault(message.from_user.id, {})
    try:
        count = int(message.text.strip())
    except ValueError:
        msg = bot.send_message(message.chat.id, "Нужно ввести число.")
        bot.register_next_step_handler(msg, process_count)
        return

    state["count"] = count
    mode = state["mode"]
    if mode == "movie_search":
        data = search_movies(state.get("title", ""), limit=count, media_type=state.get("type"), genre=state.get("genre", ""))
        state["results"] = data.get("docs", [])[:count]
        show_results(message, state)
        return

    if mode == "movie_by_rating":
        msg = bot.send_message(message.chat.id, "Введите минимальный рейтинг:")
        bot.register_next_step_handler(msg, process_rating)
        return

    if mode in ("low_budget_movie", "high_budget_movie"):
        msg = bot.send_message(message.chat.id, "Введите бюджет числом:")
        bot.register_next_step_handler(msg, process_budget)
        return

def process_rating(message):
    state = user_state.setdefault(message.from_user.id, {})
    try:
        rating = float(message.text.strip())
    except ValueError:
        msg = bot.send_message(message.chat.id, "Нужно ввести число.")
        bot.register_next_step_handler(msg, process_rating)
        return

    data = search_by_rating(
        min_rating=rating,
        max_rating=10,
        genre=state.get("genre", ""),
        limit=state.get("count", 10),
        media_type=state.get("type")
    )
    state["results"] = data.get("docs", [])[:state.get("count", 10)]
    show_results(message, state)

def process_budget(message):
    state = user_state.setdefault(message.from_user.id, {})
    try:
        budget = int(message.text.strip())
    except ValueError:
        msg = bot.send_message(message.chat.id, "Нужно ввести число.")
        bot.register_next_step_handler(msg, process_budget)
        return

    mode = state["mode"]
    if mode == "low_budget_movie":
        data = search_by_budget(
            max_budget=budget,
            genre=state.get("genre", ""),
            limit=state.get("count", 10),
            media_type=state.get("type")
        )
    else:
        data = search_by_budget(
            min_budget=budget,
            genre=state.get("genre", ""),
            limit=state.get("count", 10),
            media_type=state.get("type")
        )
    state["results"] = data.get("docs", [])[:state.get("count", 10)]
    show_results(message, state)

def show_results(message, state):
    results = state.get("results", [])
    if not results:
        bot.send_message(message.chat.id, "Ничего не найдено.")
        return

    for item in results:
        save_item(message.from_user.id, item)

    state["page"] = 0
    text = card_text(results[0])[:4096]
    sent = bot.send_message(message.chat.id, text, reply_markup=pager(0, len(results)))
    state["message_id"] = sent.message_id

@bot.callback_query_handler(func=lambda call: call.data.startswith("page:"))
def page_handler(call):
    bot.answer_callback_query(call.id)
    state = user_state.get(call.from_user.id)
    if not state or "results" not in state:
        return
    page = int(call.data.split(":")[1])
    results = state["results"]
    if 0 <= page < len(results):
        state["page"] = page
        try:
            bot.edit_message_text(
                card_text(results[page])[:4096],
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=pager(page, len(results))
            )
        except Exception:
            pass

def history_date_handler(message):
    rows = get_history(message.from_user.id, message.text.strip())
    if not rows:
        bot.send_message(message.chat.id, "История за эту дату не найдена.")
        return

    for row in rows:
        history_id, search_date, title, description, rating, year, genre, age_rating, poster, viewed = row
        text = (
            f"Дата поиска: {search_date}\n"
            f"Название фильма/сериала: {title}\n"
            f"Описание фильма/сериала: {description}\n"
            f"Рейтинг: {rating}\n"
            f"Год производства: {year}\n"
            f"Жанр: {genre}\n"
            f"Возрастной рейтинг: {age_rating}\n"
            f"Постер: {poster}"
        )
        bot.send_message(message.chat.id, text, reply_markup=history_actions(history_id, bool(viewed)))

@bot.callback_query_handler(func=lambda call: call.data.startswith(("viewed:", "unviewed:")))
def history_status_handler(call):
    bot.answer_callback_query(call.id)
    action, hid = call.data.split(":")
    set_viewed(int(hid), action == "viewed")
    bot.answer_callback_query(call.id, "Статус обновлён")

if __name__ == "__main__":
    init_db()
    bot.infinity_polling()