from utils import get_env_variable, get_service_url
from flask import Flask, request
from Queue import Queue
import requests
import json
from telepot import Bot, glance

TELEGRAM_API_TOKEN = get_env_variable('TELEGRAM_API_TOKEN')
BASE_URL = get_env_variable('BASE_URL')
PORT = get_env_variable('PORT')
MODE = get_env_variable('MODE')

bot = Bot(TELEGRAM_API_TOKEN)

# outbox
def send_message_telegram(msg):
    keyboard = None
    if 'keyboard' in msg.keys():
      keyboard = {'keyboard': [msg['keyboard']],
                  'one_time_keyboard': True,
                  'resize_keyboard': True}
    bot.sendMessage(msg['chat_id'], msg['text'], reply_markup=keyboard)


if __name__ == '__main__':

    print 'starting ' + __file__ + '...'

    app = Flask(__name__)
    update_queue = Queue()

    # inbox
    @app.route('/' + TELEGRAM_API_TOKEN, methods=['GET', 'POST'])
    def pass_update():
        update_queue.put(request.data)  # pass update to bot
        return 'OK'

    def on_chat_message(msg):
        msg = json.dumps(msg)
        reply = requests.post(
          "{}/{}".format(get_service_url('dispatcher'), 'inbox'), json=msg)


    if MODE == 'dev':
        bot.notifyOnMessage({'normal': on_chat_message}, run_forever=True)
    else:
        bot.notifyOnMessage({'normal': on_chat_message}, source=update_queue)
        bot.setWebhook(BASE_URL + '/' + TELEGRAM_API_TOKEN)
        app.run(host='0.0.0.0', port=int(PORT), debug=True)
