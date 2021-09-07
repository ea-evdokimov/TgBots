import time
import datetime

#отправка сообщения всем пользователям
def regular_send(group):
    # пока что каждые 2 минуты из состояния wait_task переходим в get_task
    if datetime.datetime.now().minute % 2 == 0:
        users = group.sql_req("SELECT `user_id` FROM `users` WHERE =gid")
        for user in users:
            user_obj = group.new_user(user["user_id"])
            
            if user_obj.status == "wait_task":            
                user_obj.variables["cur_day_correct_answers"] = 0            
                user_obj.kb.add_button("К практике!")
                user_obj.kb.inline=True
                user_obj.status = "get_task"
                user_obj.send("Пришло время решать новые задачи, начнем?", send_kb = True)        
        
        return

    if group.variables["need_send"] != "":
        users = group.sql_req("SELECT `user_id` FROM `users` WHERE =gid")
        for user in users:
            user_obj = group.new_user(user["user_id"])
            user_obj.send("Сообщение от организатора:\n{}".format(group.variables["need_send"]), send_kb = True)        
        
        group.variables["need_send"] = ""
        return
