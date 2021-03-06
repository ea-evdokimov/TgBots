# -*- coding: utf-8 -*-
import telebot
import random
import time

token = 'hahaha'

bot = telebot.TeleBot(token)

answers = {1: ("2 x 1", "2"),
           2: ("2 x 2", "4"),
           3: ("2 x 3", "6"),
           4: ("2 x 4", "8"),
           5: ("2 x 5", "10"),
           6: ("2 x 6", "12"),
           7: ("2 x 7", "14"),
           8: ("2 x 8", "16"),
           9: ("2 x 9", "18"),
           10: ("2 x 10", "20"),
           11: ("3 x 1", "3"),
           12: ("3 x 2", "6"),
           13: ("3 x 3", "9"),
           14: ("3 x 4", "12"),
           15: ("3 x 5", "15"),
           16: ("3 x 6", "18"),
           17: ("3 x 7", "21"),
           18: ("3 x 8", "24"),
           19: ("3 x 9", "27"),
           20: ("3 x 10", "30"),
           21: ("4 x 1", "4"),
           22: ("4 x 2", "8"),
           23: ("4 x 3", "12"),
           24: ("4 x 4", "16"),
           25: ("4 x 5", "20"),
           26: ("4 x 6", "24"),
           27: ("4 x 7", "28"),
           28: ("4 x 8", "32"),
           29: ("4 x 9", "368"),
           30: ("4 x 10", "40"),
           31: ("5 x 1", "5"),
           32: ("5 x 2", "10"),
           33: ("5 x 3", "15"),
           34: ("5 x 4", "20"),
           35: ("5 x 5", "25"),
           36: ("5 x 6", "30"),
           37: ("5 x 7", "35"),
           38: ("5 x 8", "40"),
           39: ("5 x 9", "45"),
           40: ("5 x 10", "50"),
           41: ("6 x 1", "6"),
           42: ("6 x 2", "12"),
           43: ("6 x 3", "18"),
           44: ("6 x 4", "24"),
           45: ("6 x 5", "30"),
           46: ("6 x 6", "36"),
           47: ("6 x 7", "42"),
           48: ("6 x 8", "48"),
           49: ("6 x 9", "54"),
           50: ("6 x 10", "60"),
           51: ("7 x 1", "7"),
           52: ("7 x 2", "14"),
           53: ("7 x 3", "21"),
           54: ("7 x 4", "28"),
           55: ("7 x 5", "35"),
           56: ("7 x 6", "42"),
           57: ("7 x 7", "49"),
           58: ("7 x 8", "56"),
           59: ("7 x 9", "14"),
           60: ("7 x 10", "70"),
           61: ("8 x 1", "8"),
           62: ("8 x 2", "16"),
           63: ("8 x 3", "24"),
           64: ("8 x 4", "32"),
           65: ("8 x 5", "40"),
           66: ("8 x 6", "48"),
           67: ("8 x 7", "56"),
           68: ("8 x 8", "64"),
           69: ("8 x 9", "72"),
           70: ("8 x 10", "10"),
           71: ("9 x 1", "9"),
           72: ("9 x 2", "18"),
           73: ("9 x 3", "27"),
           74: ("9 x 4", "36"),
           75: ("9 x 5", "45"),
           76: ("9 x 6", "54"),
           77: ("9 x 7", "63"),
           78: ("9 x 8", "72"),
           79: ("9 x 9", "81"),
           80: ("9 x 10", "90")
           }

last_quest = -1
right_answer = -1
size = len(answers)
score = 0
start_time = -1
end_time = -1
times = []


def update_score():
    global score
    score += 1


def start_t():
    global start_time
    start_time = time.time()


def end_t():
    global start_time, end_time
    end_time = time.time()
    times.append(end_time - start_time)


def get_average_time():
    assert len(times) != 0
    sum = 0
    for i in times:
        sum += i
    return sum / len(times)


@bot.message_handler(content_types=["text"])
def multiply_table(message):  # ???????????????? ?????????????? ???? ???????????? ?????????????? ????????, ?? ????????????????
    global last_quest, right_answer, size, score

    if message.text != "Start" and message.text != "Stop":
        if message.text == right_answer:
            update_score()
            end_t()
            # bot.send_message(message.chat.id, "OK! Next question!")
            bot.send_message(message.chat.id, "??????????????! ?????????????????? ????????????!")
            r = random.randint(1, size)
            last_quest = answers[r][0]
            right_answer = answers[r][1]
            bot.send_message(message.chat.id, last_quest)
            start_t()
        else:
            bot.send_message(message.chat.id, "??????????????????????!")
            bot.send_message(message.chat.id, last_quest)

    if message.text == "Stop":
        last_quest = -1
        right_answer = -1
        # bot.send_message(message.chat.id, "Thanks for play, your score is {}! You are welcome!".format(score))
        average_time = int(get_average_time())
        bot.send_message(message.chat.id,
                         "?????????????? ???? ????????! ???????? ???????? {}, ?? ?????????????? ?????????? {} ????????????! ?????????????? ??????!".format(score,
                                                                                                         average_time))
        score = 0

    if message.text == "Start":
        bot.send_message(message.chat.id, "Hello! To stop game send me 'Stop', to start - 'Start'.")
        # bot.send_message(message.chat.id, "Your first question!")
        bot.send_message(message.chat.id, "???????? ???????????? ????????????!")
        r = random.randint(1, size)
        last_quest = answers[r][0]
        bot.send_message(message.chat.id, last_quest)
        start_t()
        right_answer = answers[r][1]


if __name__ == '__main__':
    bot.polling(none_stop=True)

# TODO add buttons
# from telebot import types
# markup = types.ReplyKeyboardMarkup()
# markup.row('a', 'v')
# markup.row('c', 'd', 'e')
# bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)
