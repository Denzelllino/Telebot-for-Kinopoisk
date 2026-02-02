from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS, BOT_TOKEN
from loader import bot, BOT_INFO

from Telegrambot.api.kinopoisk_api import random_movie_request


def random_movie():
    """
    Выполняет запрос к API Кинопоиска с помощью функции random_movie_request,
    для получения данных о случайном фильме.
    Затем проверяет корректность полученных данных с помощью movie_chek.

    Возвращает:
        dict: Данные о фильме, полученные с API и прошедшие проверку.
    """

    data = random_movie_request()
    print(data)
    data = movie_chek(data)
    return data


def movie_chek(data_film):
    """
    Проверяет, что в данных фильма присутствует хотя бы одно из названий: 'name' или 'alternativeName'.
    Если названия отсутствуют, запрашивает данные снова, рекурсивно вызывая random_movie().

    Аргументы:
        data_film (dict): Данные фильма, полученные от API.

    Возвращает:
        dict: Корректные данные фильма с доступным названием.
    """

    if (
        (data_film["name"] is not None) or data_film["alternativeName"] is not None
    ) and (data_film["rating"]["kp"] != 0 or data_film["rating"]["imdb"] != 0):
        return data_film
    else:
        return random_movie()


@bot.message_handler(commands=["random"])
def random_film(message: Message):
    """
    Обработчик команды '/random' в Telegram боте.
    При вызове отправляет пользователю информацию о случайном фильме:
    - Предлагает фильм к просмотру
    - Показывает постер, если он есть
    - Выводит название (основное или альтернативное)
    - Показывает рейтинг Кинопоиска и IMDb
    - Отправляет описание, если оно доступно

    Аргументы:
        message (Message): Объект сообщения Telegram API, содержащий данные о чате и пользователе.
    """

    res = random_movie()

    bot.send_message(message.chat.id, "Я предлагаю к просмотру фильм: ")
    try:
        image_url = res["poster"]["url"]
        bot.send_photo(message.chat.id, photo=image_url)
    except:
        Exception(bot.send_message(message.chat.id, "Постер фильма не найден."))
    if res["name"] is not None:
        bot.send_message(message.chat.id, f"Название: {res['name']}")
    elif res["alternativeName"] is not None:
        bot.send_message(message.chat.id, f"Название: {res['alternativeName']}")
    else:
        bot.send_message(message.chat.id, f"Название фильма неизвестно")
    bot.send_message(message.chat.id, f"Рейтинг Кинопоиска - {res['rating']['kp']}")
    bot.send_message(
        message.chat.id, f"Пользовательский рейтинг - {res['rating']['imdb']}"
    )
    if res["description"] is not None:
        bot.send_message(message.chat.id, f"Описание - {res['description']}")
    else:
        bot.send_message(message.chat.id, "Описания к фильму нет.")
