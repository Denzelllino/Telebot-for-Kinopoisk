from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("Поиск фильма по названию", callback_data="movie_search"))
    kb.row(InlineKeyboardButton("Фильмы по рейтингу", callback_data="movie_by_rating"))
    kb.row(InlineKeyboardButton("Фильмы с низким бюджетом", callback_data="low_budget_movie"))
    kb.row(InlineKeyboardButton("Фильмы с высоким бюджетом", callback_data="high_budget_movie"))
    kb.row(InlineKeyboardButton("История поиска фильмов", callback_data="history"))
    return kb

def content_type_kb():
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("Фильмы", callback_data="type:movie"),
        InlineKeyboardButton("Сериалы", callback_data="type:tv-series")
    )
    return kb

def pager(page, total):
    kb = InlineKeyboardMarkup()
    row = []
    if page > 0:
        row.append(InlineKeyboardButton("⬅️", callback_data=f"page:{page-1}"))
    if page < total - 1:
        row.append(InlineKeyboardButton("➡️", callback_data=f"page:{page+1}"))
    if row:
        kb.row(*row)
    kb.row(InlineKeyboardButton("Назад в меню", callback_data='base_menu'))
    return kb

def history_actions(history_id, viewed):
    kb = InlineKeyboardMarkup()
    if viewed:
        kb.row(
            InlineKeyboardButton("✅ Просмотрено", callback_data=f"viewed:{history_id}"),
            InlineKeyboardButton("◻️ Не просмотрено", callback_data=f"unviewed:{history_id}")
        )
    else:
        kb.row(
            InlineKeyboardButton("◻️ Просмотрено", callback_data=f"viewed:{history_id}"),
            InlineKeyboardButton("✅ Не просмотрено", callback_data=f"unviewed:{history_id}")
        )
    return kb

def back_to_menu():
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("Назад в меню", callback_data='base_menu'))
    return kb