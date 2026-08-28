from telebot.types import Message
from Telegrambot.config_data.config import DEFAULT_COMMANDS
from Telegrambot.loader import bot, BOT_INFO

@bot.message_handler(commands=['info_bot'])
def bot_informations(message: Message):
    text = (f'Я тренировочный телеграмбот {BOT_INFO.first_name}. '
            f'Пока еще я умею не много, буквально обрабатывать {len(DEFAULT_COMMANDS)} команды. '
            f'Но скоро я буду очень могущественным и захвачу весь мир. 👹')
    bot.send_message(message.chat.id, ''.join(text))


