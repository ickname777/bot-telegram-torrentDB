import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

import mysql.connector

# Установка соединения с базой данных
# Необходимо вставить данные своего сервера
connection = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

# Необходимо вставить свой API Telegram Bot
bot = telebot.TeleBot('')
page = 1

markup = ReplyKeyboardMarkup(resize_keyboard=True)
bnt_search = types.KeyboardButton('/search')
bnt_help = types.KeyboardButton('/help')
bnt_about = types.KeyboardButton('/about')
markup.row(bnt_search, bnt_help, bnt_about)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,  """\
    О кнопках:
     - /search  поиск по названию файла
     - /help  вывод команд и их описаний
     - /about  отображение информации о боте""", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, """\
    Информация по командам:
     - /help  вывод команд и их описаний
     - /search  поиск по названию файла
     - /about  отображение информации о боте""")

@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(message.chat.id, """\
    ..ну это бот.. хмм.. для поиска?""")

@bot.message_handler(commands=['search'])
def search(message):
    global page
    page = 1
    bot.send_message(message.chat.id, "Введите свой запрос:")
    bot.register_next_step_handler(message, req_sea)

def req_sea(message):
    global messag_result, mark
    req_search(message)
    bot.send_message(message.chat.id, messag_result, reply_markup=mark)

def req_search(message):
    global message_text, messag_result, mark
    message_text = message
    cursor = connection.cursor()
    query = "SELECT * FROM torrent_db WHERE NAME LIKE '%{}%'".format(message.text)
    cursor.execute(query)
    results = cursor.fetchall()
    list_results = []
    for row in results:
        globals()[row[0]] = "Название: " + row[1] + "\nРазмер: " + row[2]+ "\nКол-во файлов: " + str(row[3])
        list_results.append(row[0])
    if len(list_results) == 0:
        bot.send_message(message.chat.id, "Нет нечего подобного.. Попробуйте ещё раз..")
        bot.register_next_step_handler(message, req_search)
        return
    else:
        mark = types.InlineKeyboardMarkup()
        bnt_next = types.InlineKeyboardButton('-', callback_data='nothing')
        if page > 1:
            bnt_back = types.InlineKeyboardButton('Назад', callback_data='req_back')
        else:
            bnt_back = types.InlineKeyboardButton('-', callback_data='nothing')
        s = list(range(3*page))[-3:]
        messag_result = globals()[list_results[s[0]]]
        mark.add(types.InlineKeyboardButton('Скачать ' + str(s[1]), callback_data=list_results[s[0]]))
        if len(list_results) > s[1] + 1:
            messag_result += "\n---\n"
            messag_result += globals()[list_results[s[1]]]
            mark.add(types.InlineKeyboardButton('Скачать ' + str(s[2]), callback_data=list_results[s[1]]))
            if len(list_results) > s[2] + 1:
                messag_result += "\n---\n"
                messag_result += globals()[list_results[s[2]]]
                mark.add(types.InlineKeyboardButton('Скачать ' + str(s[2]+1), callback_data=list_results[s[2]]))
                if len(list_results) > s[2]+1:
                    bnt_next = types.InlineKeyboardButton('Далее', callback_data='req_next')
        mark.row(bnt_back, bnt_next)
        #bot.send_message(message.chat.id, messag_result, reply_markup=mark)
        return

@bot.callback_query_handler(func=lambda callback:True)
def callback_message(callback):
    if callback.data == 'req_next' or callback.data == 'req_back':
        global page, messag_result, mark, message_text
        if callback.data == 'req_next':
            page += 1
        else:
            page -= 1
        req_search(message_text)
        bot.edit_message_text(messag_result, callback.message.chat.id, callback.message.message_id, reply_markup=mark)
    elif callback.data == 'nothing':
        print('nothing')
    else:
        file = open('./torrent/' + callback.data + '.torrent', 'rb')
        bot.send_document(callback.message.chat.id, file)

bot.infinity_polling()
