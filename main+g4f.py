import telebot
import g4f

# Создаем экземпляр телеграм бота
bot = telebot.TeleBot("6597127566:AAHtsyPwdBzidgv9MCXAPUwchk8QfeAtG3c")

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
        response = g4f.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=user_messages
        )
        
        # Получаем ответ и отправляем его обратно пользователю
        bot.reply_to(message, response)

    except Exception as e:
        # Выводим в консоль ошибку и отправляем сообщение об ошибке пользователю
        print(f"Error: {str(e)}")
        bot.reply_to(message, f"Произошла ошибка при обработке вашего запроса. Попробуйте отправить его снова или вернитесь позднее.")

# Запускаем телеграм бота
bot.polling()