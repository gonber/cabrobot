from utils import get_env_variable
from flask import Flask, request
import json
from gateway_telegram import send_message_telegram

PORT = get_env_variable('DISPATCHER_PORT')

app = Flask(__name__)

@app.route('/dispatcher/inbox', methods=['POST'])
def inbox_new():
    msg = json.loads(request.get_json())
    reply = {}
    reply['text'] = 'your text was ' + msg['text']
    reply['chat_id'] = msg['chat']['id']
    send_message_telegram(reply)
    return 'OK'

if __name__ == '__main__':

    print 'starting ' + __file__ + '...'

    app.run(port=int(PORT), debug=True)
