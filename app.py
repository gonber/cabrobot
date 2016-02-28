import sys
import os
import time
import pprint
import telepot

from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
try:
    load_dotenv(dotenv_path)
except:
    print "no .env found"

def handle(msg):
    pprint.pprint(msg)
    # Do your stuff here ...


# Getting the token from command-line is better than embedding it in code,
# because tokens are supposed to be kept secret.
TOKEN = os.environ.get('TELEGRAM_API_TOKEN') # sys.argv[1]
bot = telepot.Bot(TOKEN)
bot.notifyOnMessage(handle)
print 'Listening ...'

# Keep the program running.
while 1:
    time.sleep(10)
