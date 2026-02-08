import json

from telebot.types import Message
import telebot

from config_data.config import DEFAULT_COMMANDS, BOT_TOKEN
from loader import bot, BOT_INFO

from Telegrambot.api.kinopoisk_api import search_name_film

@bot.message_handler(commands=["search"])
def search_film(message: Message):
    bot.send_message(message.chat.id, "Давай найдем твой фильм, напиши мне его название"
                                      "(пока по русски, в последующем я научусь отличать русские"
                                      "и английские названия). ")
    bot.register_next_step_handler(message, get_name)

def get_name(message: Message):
    name = message.text

    data = search_name_film(name)

    print(json.dumps(data, indent=4, ensure_ascii=False))
    print(data["docs"][0]['description'])

    bot.send_message(message.chat.id, "Я уверен Вы искали именно этот фильм: ")
    try:
        image_url = data["docs"][0]["poster"]["url"]
        bot.send_photo(message.chat.id, photo=image_url)
    except:
        Exception(bot.send_message(message.chat.id, "Постер фильма не найден."))
    if data["docs"][0]["name"] is not None:
        bot.send_message(message.chat.id, f"Название: {data["docs"][0]['name']}")
    elif data["docs"]["alternativeName"] is not None:
        bot.send_message(message.chat.id, f"Название: {data["docs"][0]['alternativeName']}")
    else:
        bot.send_message(message.chat.id, f"Название фильма неизвестно")
    bot.send_message(message.chat.id, f"Рейтинг Кинопоиска - {data["docs"][0]['rating']['kp']}")
    bot.send_message(
        message.chat.id, f"Пользовательский рейтинг - {data["docs"][0]['rating']['imdb']}"
    )
    if data["docs"][0]["description"] is not None:
        bot.send_message(message.chat.id, f"Описание - {data["docs"][0]['description']}")
    else:
        bot.send_message(message.chat.id, "Описания к фильму нет.")

