import sys
import os
import telepot
import pprint
from telepot.delegate import per_chat_id, create_open

from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

users = list()
users.append(0)

class CabRobot(telepot.helper.ChatHandler):
    def __init__(self, seed_tuple, timeout):
        super(CabRobot, self).__init__(seed_tuple, timeout)
        self._state = 'init'
        self._location = 'unknown'
        self._role = 'unknown'

    def on_chat_message(self, msg):
        content_type, _, _ = telepot.glance(msg)
        users.append(1)
        if self._state == 'init':
            if content_type == 'location':
                self._location = msg['location']
                self._state = 'known_location'

                show_keyboard = {'keyboard': [['ride','drive']],
                                 'resize_keyboard': True,
                                 'one_time_keyboard': True}
                self.sender.sendMessage('do you want to ride or drive?',
                    reply_markup=show_keyboard)
            else:
                self.sender.sendMessage('start by sharing your location')
        elif self._state == 'known_location':
            if msg['text'] == 'ride':
                self._role = 'rider'
            elif msg['text'] == 'drive':
                self._role = 'driver'
            print self._role

TOKEN = os.environ.get('TELEGRAM_API_TOKEN')

bot = telepot.DelegatorBot(TOKEN, [
    (per_chat_id(), create_open(CabRobot, timeout=10)),
])
bot.notifyOnMessage()#run_forever=True)

# Keep the program running.
import time
while 1:
    time.sleep(1)
    print users
