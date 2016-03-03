from utils import get_env_variable
from flask import Flask, request
from Queue import Queue
from telepot import Bot, glance

TELEGRAM_API_TOKEN = get_env_variable('TELEGRAM_API_TOKEN')
BASE_URL = get_env_variable('BASE_URL')
HOST = get_env_variable('HOST')
PORT = get_env_variable('PORT')

app = Flask(__name__)
update_queue = Queue()

@app.route('/' + TELEGRAM_API_TOKEN, methods=['GET', 'POST'])
def pass_update():
    update_queue.put(request.data)  # pass update to bot
    return 'OK'

def on_chat_message(msg):
    content_type, chat_type, chat_id = glance(msg)
    print 'Normal Message:', content_type, chat_type, chat_id

bot = Bot(TELEGRAM_API_TOKEN)

if __name__ == '__main__':

    print 'starting ' + __file__ + '...'

    if HOST == 'localhost':
        bot.notifyOnMessage({'normal': on_chat_message}, run_forever=True)
    else:
        bot.notifyOnMessage({'normal': on_chat_message}, source=update_queue)
        bot.setWebhook(BASE_URL + '/' + TELEGRAM_API_TOKEN)
        app.run(host='0.0.0.0', port=int(PORT), debug=True)
