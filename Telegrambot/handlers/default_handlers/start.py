from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot, BOT_INFO


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.full_name}!')
    bot.send_message(message.chat.id, f'Меня зовут {BOT_INFO.first_name}. Я буду твоим личным помощником '
                                      f'в (чем то там с чем мы еще определимся)')

