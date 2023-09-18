import telebot
from telebot import types

TOKEN = '6597127566:AAHtsyPwdBzidgv9MCXAPUwchk8QfeAtG3c'
bot = telebot.TeleBot(TOKEN)

# Список состояний пользователей
user_states = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_states[user_id] = "main_menu"
    bot.send_message(message.chat.id, "Привет! Я бот для использования нейросетей")
    send_main_menu(message.chat.id)

# Функция для отправки основного меню
def send_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Далее")
    markup.add(item)
    bot.send_message(chat_id, "Нажми 'Далее', чтобы продолжить:", reply_markup=markup)

# Функция для отправки кнопок выбора
def send_choice_buttons(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("ChatGPT")
    item2 = types.KeyboardButton("YaGPT")
    item3 = types.KeyboardButton("AI")
    markup.row(item1, item2, item3)
    bot.send_message(chat_id, "Выбери одну из доступных опций", reply_markup=markup)

# Обработчик кнопки "Далее"
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "main_menu" and message.text == "Далее")
def continue_button(message):
    user_id = message.from_user.id
    user_states[user_id] = "awaiting_choice"
    send_choice_buttons(message.chat.id)

# Обработчик выбора кнопок 1, 2 или 3
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "awaiting_choice" and message.text in ["ChatGPT", "YaGPT", "AI"])
def handle_choice_message(message):
    user_id = message.from_user.id
    choice = message.text
    handle_choice(user_id, choice)
    user_states[user_id] = "awaiting_main_menu"
    send_return_to_main_menu(message.chat.id)

# Функция для обработки выбора кнопок
def handle_choice(user_id, choice):
    if choice == "ChatGPT":
        bot.send_message(user_id, "Вы выбрали ChatGPT")
    elif choice == "YaGPT":
        bot.send_message(user_id, "Вы выбрали YaGPT")
    elif choice == "AI":
        bot.send_message(user_id, "Вы выбрали AI")

# Функция для отправки кнопки "Вернуться к выбору доступных опций" и "Завершить диалог"
def send_return_to_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Вернуться к выбору доступных опций")
    item2 = types.KeyboardButton("/stop")
    markup.add(item1, item2)
    bot.send_message(chat_id, "Выбери действие:", reply_markup=markup)

# Обработчик выбора действия после выбора опции
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "awaiting_main_menu" and message.text in ["Вернуться к выбору доступных опций", "/stop"])
def handle_return_or_stop(message):
    user_id = message.from_user.id
    if message.text == "Вернуться к выбору доступных опций":
        user_states[user_id] = "main_menu"
        send_main_menu(message.chat.id)
    elif message.text == "/stop":
        del user_states[user_id]
        bot.send_message(message.chat.id, "Диалог завершен. Вы можете начать новый, написав /start.")

if __name__ == "__main__":
    bot.polling(none_stop=True)