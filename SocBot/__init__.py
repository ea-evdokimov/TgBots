import importlib
import time

pkg = "library.bots.edu."
crn = importlib.import_module(pkg + "cron")
# там описаны основные функции
fu = importlib.import_module(pkg + "functions")
importlib.reload(crn)
importlib.reload(fu)

#при отправке сообщения
def process(user):
    if user.message == '/help':
        fu.help(user)
        return
    
    # нужно ли
    if user.message == '/start' and user.status != "start":
        user.kb.add_button("/restart")
        user.kb.inline=True
        user.send("Ты хочешь начать заново? Все данные сотрутся", send_kb=True)
        return
    
    if user.message == '/restart':
        user.variables.clear_all()
        fu.start(user)
        return

    if user.message == "/admin" and user.status != "admin":
        user.send("Введи пароль")
        user.variables["last_message_sent"] = user.message
        return

    if user.variables["last_message_sent"] == "/admin" and user.status != "admin":
        password = "password"

        if user.message == password:
            user.status = "admin"
            user.kb.add_button("/send_all")
            user.kb.inline=True
            user.send("Можешь использовать /send_all", send_kb=True) 
        else:
            user.send("Неправильно. А ты точно админ? Если нет, придется перезапустится", send_kb=True)
        return

    if user.status == "admin":
        fu.admin(user)
        return

    if user.status == "start":
        fu.start(user)
        return

    elif user.status == "get_name":
        fu.get_name(user)
        return

    elif user.status == "submit_name":
        fu.submit_name(user)
        return

    elif user.status == "get_task":
    
        if user.message == '/stat' or user.message == "Получить статистику!":
            fu.get_stat(user)
            return
        
        if user.message == '/task' or user.message == 'Да!' or user.message == "К практике!":
            fu.get_task(user)
            return
        
        else:
            if user.message == 'Нет':
                return

            user.kb.add_button("Да!")
            user.kb.add_button("Нет")
            user.kb.inline=True
            user.send("Ты можешь получить задание, хочешь?", send_kb=True)

    elif user.status == "submit_task":
        fu.submit_task(user)

    # из этого статуса выходят только с помощью cron
    elif user.status == "wait_task":
        if user.message == '/stat' or user.message == 'Получить статистику!':
            fu.get_stat(user)
        else:
            fu.wait_task(user)

    else:
        user.status = "start"

def cron(group):
    crn.regular_send(group)