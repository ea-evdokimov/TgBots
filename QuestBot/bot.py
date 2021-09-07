import logging
import json
import time
import datetime

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update

all_tasks = ['1', '2', '3', '4', '5', '6']

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, SOLVING, SUBMITTING, REG = range(4)

class PollingBot:
    def __init__(self, quests_path):
        self.__quests = get_json(quests_path)

    def start(self, updater: Update, context: CallbackContext):
        updater.message.reply_text(
            self.__quests['entry_point']
        )
        return REG

    def main(self, updater: Update, context: CallbackContext):
        user_data = context.user_data
        reply_keyboard = [user_data['keyboard'], ['Ваш прогресс']]

        updater.message.reply_text(
            'Выберите задачу',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )

        return CHOOSING

    def reg(self, updater: Update, context: CallbackContext):
        
        user_data = context.user_data
        text = updater.message.text

        user_data['name'] = text
        user_data['score'] = 0
        user_data['step_answ'] = ''
        user_data['progress'] = []
        user_data['last_time'] = 0.0
        user_data['last_quest'] = ''
        user_data['keyboard'] = all_tasks 
 
        reply_keyboard = [user_data['keyboard']]

        updater.message.reply_text(
            'Выберите задачу',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )

        return CHOOSING


    def choosing_quest(self, updater: Update, context: CallbackContext):
        user_data = context.user_data
        text = updater.message.text

        response = self.get_response(text)

        user_data['step_answ'] = response['right_answ']
        user_data['last_quest'] = text
        
        y = time.time()
        user_data['last_time'] = y

        updater.message.reply_text(response['quest'])
        if 'pic' in response.keys():
            updater.message.reply_photo(response['pic'])

        if response['open_quest'] == 'True':
            return SOLVING
        
        name_list = []
        for i, answ in enumerate(response['answ']):
            if i % 2 == 0:
                name_list.append([])
            name_list[i // 2].append(answ['name'])

            
        name_list.append(['Назад'])

        updater.message.reply_text(
            'Выберите один вариант ответа',
            reply_markup=ReplyKeyboardMarkup(name_list, one_time_keyboard=True)
        )

        return SOLVING

    def solving(self, updater: Update, context: CallbackContext):
        user_data = context.user_data
        text = updater.message.text
        
        if user_data['step_answ'].find(text.lower()) != -1: 
            user_data['keyboard'].remove(user_data['last_quest'])

            user_data['progress'].append('\n' + user_data['last_quest'] + ':' + text + ' - ' + 'OK!')
            
            x = 1.0 - (time.time() - user_data['last_time']) / (20.0 * 60.0)
            user_data['score'] += x

            reply_keyboard = [user_data['keyboard'], ['Ваш прогресс']]
            updater.message.reply_text(
                'Задача решена!',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            )        
        
        else:
            user_data['score'] -= 0.5
            user_data['progress'].append('\n' + user_data['last_quest'] + ':' + text + ' - ' + 'FAIL!')
            
            reply_keyboard = [user_data['keyboard'], ['Ваш прогресс']]
            
            updater.message.reply_text(
                'К сожалению не верно!',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            )

        return CHOOSING

    def check_progress(self, updater: Update, context: CallbackContext):
        reply_keyboard = [['Начать заново'], ['Закончить и сохранить ответы'], ['Назад']]

        user_data = context.user_data
        text = updater.message.text

        if 'progress' != '':
            order_str = ''.join(user_data['progress'])
        else:
            order_str = 'Вы ещё ничего не решили'

        updater.message.reply_text(
            order_str,
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )

        return CHOOSING

    def clear_progress(self, updater: Update, context: CallbackContext):
        user_data = context.user_data
        text = updater.message.text

        user_data['progress'] = []

        reply_keyboard = [user_data['keyboard']]

        updater.message.reply_text(
            'Прогресс очищен',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )

        return CHOOSING

    def send_progress(self, updater: Update, context: CallbackContext):
        user_data = context.user_data
        text = updater.message.text

        file = open('ans/{}.txt'.format(user_data['name']), 'w')
        str1 = '\n'.join(user_data['progress'])
        file.write(str1 + '\n SCORE : {}'.format(user_data['score']))
        file.close()

        print('New answer from {}'.format(user_data['name']))
        updater.message.reply_text(
            'Прогресс записан! Ваш счет: {}'.format(round(user_data['score'], 2))
        )
        return

    def get_response(self, text: str):
        if text:
            return self.__quests['quests'][text]
        else:
            return


def get_json(path):
    file = open(path, 'r')
    return json.load(file)

def main():
    settings = get_json('data/settings.json')
    updater = Updater(settings['token'])
    dispatcher = updater.dispatcher

    bot = PollingBot('data/quests1.json')

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', bot.start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(1|2|3|4|5|6)$'),
                    bot.choosing_quest
                ),
                MessageHandler(
                    Filters.regex('Ваш прогресс'),
                    bot.check_progress
                ),
                MessageHandler(
                    Filters.regex('Закончить и сохранить ответы'),
                    bot.send_progress
                ),
                MessageHandler(
                    Filters.regex('Начать заново'),
                    bot.clear_progress
                ),
                MessageHandler(
                    Filters.regex('Назад'),
                    bot.main
                ),
            ],
            SOLVING: [
                MessageHandler(
                    Filters.regex('Назад$'),
                    bot.main
                ),
                MessageHandler(
                    Filters.regex('^(?!Назад$)'),
                    bot.solving
                )
            ],
            REG: [
                MessageHandler(
                    Filters.all,
                    bot.reg
                )
            ]
        },
        fallbacks=[CommandHandler('start', bot.start)]
    )

    dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
