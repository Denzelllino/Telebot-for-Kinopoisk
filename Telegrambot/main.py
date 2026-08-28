from loader import bot
import handlers  # noqa

from database.db import init_db
from utils.set_bot_commands import set_default_commands

if __name__ == "__main__":
    init_db()
    set_default_commands(bot)
    bot.infinity_polling()
