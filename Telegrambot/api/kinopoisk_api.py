import requests, json
from Telegrambot.config_data.config import KINOPOISK_API_KEY

url = 'https://api.kinopoisk.dev/'

function = {'random': 'v1.4/movie/random'}

headers = {
        "accept": "application/json",
        "X-API-KEY": KINOPOISK_API_KEY
    }

def random_movie_request():
    """
    Выполняет GET-запрос к API Кинопоиска для получения данных случайного фильма.

    Использует endpoint 'v1.4/movie/random' API Кинопоиска.

    Возвращает:
        dict: Распарсенный JSON-ответ с данными о случайном фильме.

    Исключения:
        requests.exceptions.RequestException: В случае проблем с HTTP-запросом.
        json.JSONDecodeError: При ошибке декодирования JSON-ответа.
    """

    request_url = url + function['random']
    response_api = requests.get(request_url, headers=headers)
    data = json.loads(response_api.text)
    return data
