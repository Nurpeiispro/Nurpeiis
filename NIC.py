import webbrowser
import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot('7086737150:AAEyo188fBZkznW9ofk4jL1jZXCTD_qPB7U')
name = None
number = None


@bot.message_handler(commands=['start'])s
def start(message):
    bot.send_message(message.chat.id, 'Сәлем жас айтишник. Саған қалай көмек көрсете аламын')


@bot.message_handler(commands=['info'])
def info(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Біздің ресми сайт', url='https://niclandingwebsite.vercel.app/')
    btn2 = types.InlineKeyboardButton('Біздің проекттер', callback_data='project')
    btn3 = types.InlineKeyboardButton('Біздің менторлар', callback_data='mentors')
    btn4 = types.InlineKeyboardButton('Біздің тарихымыз', callback_data='history')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    file = open('./nic.png', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if(callback.data == 'project'):
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('бірінші проект', url='https://github.com/OralbekUrusbekov/project.git')
        btn2 = types.InlineKeyboardButton('екінші проект', url='https://github.com/zhneo/html-css-js')
        btn3 = types.InlineKeyboardButton('үшінші проект', url='https://github.com/baukakzs/Project-of-NIC')
        btn4 = types.InlineKeyboardButton('төртінші проект', url='https://github.com/Madik981/JS-Practice__To-Do-List')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(callback.message.chat.id, 'Біздің проекттер', reply_markup=markup)
    elif(callback.data == 'mentors'):
        bot.send_message(callback.message.chat.id, 'Негізі осы жерде менторлар туралы ақпарат болуы керек еді')
    elif(callback.data == 'history'):
        history(callback.message)
    elif(callback.data == 'babies'):
        conn = sqlite3.connect('nic babies.sql')
        cur = conn.cursor()

        cur.execute('SELECT * FROM users ')
        babies = cur.fetchall()

        information = ''
        for el in babies:
            information += f'Есімі: {el[1]}. Телефон номері: {el[2]}. Бағыты: {el[3]}\n'

        cur.close()
        conn.close()

        bot.send_message(callback.message.chat.id, information)


def project(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('бірінші проект', url='https://github.com/OralbekUrusbekov/project.git')
    btn2 = types.InlineKeyboardButton('екінші проект', url='https://github.com/zhneo/html-css-js')
    btn3 = types.InlineKeyboardButton('үшінші проект', url='https://github.com/baukakzs/Project-of-NIC')
    btn4 = types.InlineKeyboardButton('To-Do List', url='https://github.com/Madik981/JS-Practice__To-Do-List')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    bot.send_message(message.chat.id, 'Біздің проекттер', reply_markup=markup)


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://niclandingwebsite.vercel.app/')


@bot.message_handler(commands=['history'])
def history(message):
    bot.send_message(message.chat.id, 'Осы жерде клуб тарихы айтылады')

@bot.message_handler(commands=['register'])
def register(message):
    conn = sqlite3.connect('nic babies.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTs users (id int auto_increment primary key, name varchar(50), number varchar(50), put varchar(50))')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Сәлеметсіз бе! Қазір сізді тіркеймін. Атыңызды енгізіңіз:')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, f'{name} телефон номеріңізді енгізіңіз')
    bot.register_next_step_handler(message, user_number)


def user_number(message):
    global number
    number = message.text.strip()
    bot.send_message(message.chat.id, f'Қандай бағытты таңдайсыз (fronted немесе backend)')
    bot.register_next_step_handler(message, user_put)


def user_put(message):
    put = message.text.strip()
    conn = sqlite3.connect('nic babies.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, number, put) VALUES ('%s','%s','%s')" % (name, number, put))
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Сіз сәтті тіркелдіңіз! Аздаған уақытта сізбен менеджерлер баланысатын болады')


@bot.message_handler(commands=['my_babies'])
def my_babies(message):
    marcup = types.InlineKeyboardMarkup()
    marcup.add(types.InlineKeyboardButton('Тіркелушіліер туралы ақпарат', callback_data='babies'))
    file = open('./hacker.png', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=marcup)


@bot.message_handler()
def word(message):
    if (message.text.lower() == 'привет'):
        bot.send_message(message.chat.id, 'Сәлем жас айтишник. Саған қалай көмек көрсете аламын')


bot.infinity_polling()
