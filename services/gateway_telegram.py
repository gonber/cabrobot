from utils import get_env_variable
from flask import Flask, request
from Queue import Queue
import telepot
import os
import sys

app = Flask(__name__)
update_queue = Queue()

TELEGRAM_API_TOKEN = get_env_variable('TELEGRAM_API_TOKEN')
BASE_URL = get_env_variable('BASE_URL')
PORT = int(sys.argv[1])

@app.route('/' + TELEGRAM_API_TOKEN, methods=['GET', 'POST'])
def pass_update():
    update_queue.put(request.data)  # pass update to bot
    return 'OK'

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print 'Normal Message:', content_type, chat_type, chat_id

bot = telepot.Bot(TELEGRAM_API_TOKEN)

if __name__ == '__main__':

    if BASE_URL == 'localhost':
        bot.notifyOnMessage({'normal': on_chat_message}, run_forever=True)
    else:
        bot.notifyOnMessage({'normal': on_chat_message}, source=update_queue)
        bot.setWebhook(BASE_URL + '/' + TELEGRAM_API_TOKEN)

    app.run(port=PORT, debug=True)
