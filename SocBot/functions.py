import random
import io
import os.path

ext = [".jpg", ".jpeg", ".png", ".webp"]
path_img = "library/bots/edu/img/"
ALL_CARDS = 350

def help(user):
    user.send("Команды:\n/start - начать сначала(без сохранения результата)\n/help - для вывода этой странички\n/task - для получения задания\n/stat - для получения статистики", send_kb=True)


def start(user):
    user.send("Привет! Пожалуйста введи свое имя и фамилию одним сообщением в формате Иванов Иван!", send_kb = True)
    user.status = "get_name"


def get_name(user):
    user.status = "submit_name"
    user.variables["name"] = user.message
    user.kb.add_button("Да!")
    user.kb.add_button("Нет")
    user.kb.inline=True
    user.send("Твое имя - {}?".format(user.variables["name"]), send_kb = True)


def submit_name(user):
    if user.message == "Да!":
        user.status = "get_task"
        
        user.kb.add_button("Да!")
        user.kb.inline=True
        user.send("Отлично! Продолжим?", send_kb = True)

        # поля для статистики
        user.variables["all_correct_answers"] = 0
        user.variables["all_wrong_answers"] = 0
        user.variables["cur_day_correct_answers"] = 0
        user.variables["cur_day_wrong_answers"] = 0
    
    else:
        user.send("Пожалуйста, введи свое имя еще раз в формате Иванов Иван") 
        user.status = "get_name"

def get_stat(user):
    user.send("Статистика: всего правильных ответов: {}, за сегодня: {}\nнеправильных всего: {}, сегодня: {}".format(
        user.variables["all_correct_answers"], user.variables["cur_day_correct_answers"], user.variables["all_wrong_answers"], user.variables["cur_day_wrong_answers"]), send_kb = True)

def random_task():
    return random.randint(1, ALL_CARDS)

def get_task(user):
    user.variables["cur_task"] = random_task()
    pic_path = path_img + str(user.variables["cur_task"]) + "/" + str(user.variables["cur_task"])
    
    id = 0
    for exten in ext:
    	pic_ = pic_path + exten
    	if os.path.isfile(pic_):
        	id = user.upload_photo(pic_, False)
        	break
    
    q = io.open(path_img + str(user.variables["cur_task"]) + "/question.txt", "r", encoding="utf-8")
    string = "{}".format(q.read())
    user.send(string, att=id, send_kb = True)
    user.status = "submit_task"

def submit_task(user):
    a = io.open(path_img + str(user.variables["cur_task"]) + "/right_ans.txt", "r", encoding="utf-8")
    r_a = io.open(path_img + str(user.variables["cur_task"]) + "/ans_true.txt", "r", encoding="utf-8")
    w_a = io.open(path_img + str(user.variables["cur_task"]) + "/ans_false.txt", "r", encoding="utf-8")

    string = a.read()
    # вырезаем последний перевод строки
    #string = string[:-1]
    string = string.lower()
    user_message = (user.message).lower()

    if user_message == string:
        user.variables["all_correct_answers"] = int(user.variables["all_correct_answers"]) + 1
        user.variables["cur_day_correct_answers"] = int(user.variables["cur_day_correct_answers"]) + 1 
        user.send(r_a.read(), send_kb=True)
    else:
        user.variables["all_wrong_answers"] = int(user.variables["all_wrong_answers"]) + 1
        user.variables["cur_day_wrong_answers"] = int(user.variables["cur_day_wrong_answers"]) + 1
        user.send(w_a.read(), send_kb = True)
    # если лимит не исчерпан, следующие задание 
    if int(user.variables["cur_day_correct_answers"]) < 5:
        user.kb.add_button("Да!")
        user.kb.inline=True
        user.send("Следующее задание?", send_kb = True)
        user.status = "get_task"
    else:
        user.kb.add_button("Получить статистику!")
        user.status = "wait_task"
        user.send("На сегодня всё. Ты молодец, хочешь посмотреть свою статистику?", send_kb = True)


def wait_task(user):
    user.kb.add_button("Получить статистику!")
    user.send("На сегодня всё. Ты молодец, хочешь посмотреть свою статистику?", send_kb = True)


def admin(user):
    if user.message == "/send_all":
        user.send("Введи послание всем пользователям бота:", send_kb = True)
        user.variables["last_message_sent"] = user.message
    else:
        if user.variables["last_message_sent"] == "/send_all":
            user.variables["last_message_sent"] = ""
            user.group.variables["need_send"] = user.message
            user.send("Сообщение записано. Оно отправится в течение минуты", send_kb = True)
        
