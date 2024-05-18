import telebot
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

token = os.getenv('TOKEN')
me = os.getenv('ME')

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'it  works')


def send_message(message):
    bot.send_message(me, message)


bot.infinity_polling(timeout=10, long_polling_timeout=5)
bot.polling(none_stop=True)
