from telebot import types


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

btn_random = types.KeyboardButton('Посмотрим случайный фильм?')
btn_search = types.KeyboardButton('Давай найду твой фильм.')

markup.row(btn_random, btn_search)

btn_help = types.KeyboardButton('Не знаешь куда нажать? Жми сюда!')
btn_later = types.KeyboardButton('Может позже!')

markup.row(btn_later, btn_help)

remove_keyboard = types.ReplyKeyboardRemove()
