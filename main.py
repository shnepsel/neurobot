import telebot
import openai
import os
from environs import Env

# Устанавливаем URL для API OpenAI
openai.api_base = "https://api.nova-oss.com/v1" # https://api.daku.tech/v1

# Получаем API ключ OpenAI из переменной окружения
openai.api_key = "nv2-AXKSI82JfwbcyNxsasE1_NOVA_v2_0ZOQXqs5ILrHDIsQQnNX" # sk-RWFDNjE0N0I3MzEzT3BlbkFJYjVEY0JBZDBDQzRj

# Создаем экземпляр класса Env
env = Env()
 
# Читаем файл .env и загружаем из него переменные в окружение
env.read_env()

# Создаем экземпляр телеграм бота
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

# Словарь для хранения переписки с пользователями
user_chats = {}

# Обработчик команды "/start"
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Отправьте мне интересующий вас вопрос.")

# Обработчик команды "/help"
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,
                 "Вы можете отправлять запросы в OpenAI API через меня. Просто напишите мне свой запрос и я отправлю его на обработку.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, "Запрос принят в обработку.")
    try:
        user_id = message.from_user.id
        user_messages = user_chats.get(user_id, [])
        user_messages.append({"role": "user", "content": message.text})
        user_chats[user_id] = user_messages

        # Отправляем запрос в API OpenAI
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=user_messages,
            # max_tokens=350  # Максимальное количество токенов в ответе
        )
        
        # Получаем ответ и отправляем его обратно пользователю
        bot.reply_to(message, response.choices[0].message["content"])
    except Exception as e:
        # Выводим в консоль ошибку и отправляем сообщение об ошибке пользователю
        print(f"Error: {str(e)}")
        bot.reply_to(message, f"Произошла ошибка при обработке вашего запроса. Попробуйте отправить его снова или вернитесь позднее.")

# Запускаем телеграм бота
bot.polling()