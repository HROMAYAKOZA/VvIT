import telebot
import psycopg2
import datetime
from telebot import types


token = "<токен>"
bot = telebot.TeleBot(token)
schedule = types.ReplyKeyboardMarkup(resize_keyboard=True)
schedule.row("Пн", "Вт", "Ср", "Чт", "Пт", "Сб")
schedule.row("Текущая неделя", "Следующая неделя")
conn = psycopg2.connect(database="schedule_db", user="postgres",
                        password="1234", host="localhost", port="5432")
cursor = conn.cursor()
weekday = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]


def datatime(day, week):
    s = '_'*12+'\n'
    daytime = day + week*6
    cursor.execute("SELECT ls_start_time, sub_name, room_numb, full_name FROM timetable m, subjects, lesson_begin, teacher t WHERE day='%s' and m.sub_t=sub_id and sub_id=t.sub_t and les_n=start_time order by 1" % str(daytime))
    records = list(cursor.fetchall())
    for i in records:
        for j in i:
            s += f'&lt{j}&gt '
        s += "\n"
    if s.find("&lt") == -1:
        s += "<s>Нет занятий в данный день</s>\n"
    return s


def subjt():
    s = ''
    cursor.execute(
        "SELECT sub_name, full_name FROM subjects, teacher WHERE sub_id=sub_t")
    records = list(cursor.fetchall())
    for i in records:
        s += f"{i[0]} - {i[1]}\n"
    return s


@bot.message_handler(commands=['week'])
def debug(message):
    week = (message.date-1675026000)//604800+1
    if (week % 2 == 0):
        weeks = "чётная"
    else:
        weeks = "нечётная"
    bot.send_message(message.chat.id, f'Текущая неделя: {week}, {weeks}')
    # начало семестра 1675026000


@bot.message_handler(commands=['mtuci'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton("Перейти🌐", url="https://mtuci.ru/")
    keyboard.add(b1)
    bot.send_message(
        message.chat.id, 'Официальный сайт МТУСИ – https://mtuci.ru/', reply_markup=keyboard)


@bot.message_handler(commands=['find'])
def start_message(message):
    t = ''
    s = message.text.replace("/find ", "")
    if s[0] == "А":
        t += "Корпус на Авиамоторной, "
        if s[2] == "С":
            t += "спортивный зал."
        elif s[2] == "В":
            t += "вычислительный центр " + s[5] + " этаж."
        elif s[2] == "Л":
            t += "лабораторный корпус " + s[4] + " этаж."
        else:
            t += "главный корпус " + s[2] + " этаж."
    elif s[0] == "Н":
        t += "Корпус на Народном ополчении, "
        if s[2] == "С":
            t += "спортивный зал."
        elif s[2] == "В":
            t += "вычислительный центр " + s[5] + " этаж."
        elif s[2] == "Л":
            t += "лабораторный корпус " + s[4] + " этаж."
        else:
            t += "главный корпус " + s[2] + " этаж."
    else:
        t += "Кабинет не распознан"
    bot.send_message(message.chat.id, f'Кабинет {s} расположен здесь:\n{t}')


@bot.message_handler(content_types=['sticker'])
def emoji(message):
    bot.send_message(message.chat.id, "👋")


@bot.message_handler(commands=['subjects'])
def start_message(message):
    s = subjt()
    bot.send_message(message.chat.id, f'Список предметов и учителя:\n{s}')


@bot.message_handler(commands=['start'])
def debug(message):
    bot.send_message(message.chat.id, '<b>Категорически приветсвтую!</b> Здесь вы можете узнать информацию о расписании',
                     reply_markup=schedule, parse_mode="HTML")


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Данный бот умеет отображать расписание на интересующий день недели или неделю, список всех предметов в данном семестре и перенаправлять на официальный сайт МТУСИ', reply_markup=schedule)


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "пн":
        s = datatime(1, ((message.date-1675026000)//604800) % 2)
        bot.send_message(
            message.chat.id, f'Расписание на понедельник, неделя №{(message.date-1675026000)//604800+1}\n{s}', parse_mode="HTML")
    elif message.text.lower() == "вт":
        s = datatime(2, ((message.date-1675026000)//604800) % 2)
        bot.send_message(
            message.chat.id, f'Расписание на вторник, неделя №{(message.date-1675026000)//604800+1}\n{s}', parse_mode="HTML")
    elif message.text.lower() == "ср":
        s = datatime(3, ((message.date-1675026000)//604800) % 2)
        bot.send_message(
            message.chat.id, f'Расписание на среду, неделя №{(message.date-1675026000)//604800+1}\n{s}', parse_mode="HTML")
    elif message.text.lower() == "чт":
        s = datatime(4, ((message.date-1675026000)//604800) % 2)
        bot.send_message(
            message.chat.id, f'Расписание на четверг, неделя №{(message.date-1675026000)//604800+1}\n{s}', parse_mode="HTML")
    elif message.text.lower() == "пт":
        s = datatime(5, ((message.date-1675026000)//604800) % 2)
        bot.send_message(
            message.chat.id, f'Расписание на пятницу, неделя №{(message.date-1675026000)//604800+1}\n{s}', parse_mode="HTML")
    elif message.text.lower() == "сб":
        s = datatime(6, ((message.date-1675026000)//604800) % 2)
        bot.send_message(
            message.chat.id, f'Расписание на субботу, неделя №{(message.date-1675026000)//604800+1}\n{s}', parse_mode="HTML")
    elif message.text.lower() == "текущая неделя":
        s = '_'*12+'\n'
        for i in range(1, 7):
            s += str(weekday[i-1])+"\n"
            s += datatime(i, ((message.date-1675026000)//604800) % 2) + '\n'
        bot.send_message(
            message.chat.id, f'Расписание на эту неделю\n{s}', parse_mode="HTML")
    elif message.text.lower() == "следующая неделя":
        s = '_'*12+'\n'
        for i in range(1, 7):
            s += str(weekday[i-1])+"\n"
            s += datatime(i, ((message.date-1675026000)//604800+1) % 2) + '\n'
        bot.send_message(
            message.chat.id, f'Расписание на следующую неделю\n{s}', parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, 'Извините, я вас не понял.')


bot.infinity_polling()
