from utils import get_env_variable, get_service_url
from datetime import datetime
from flask import Flask, request
import json
from gateway_telegram import send_message_telegram
from users import Users

PORT = get_env_variable('DISPATCHER_PORT')

PERISHABLE_FIELDS = ['current_location', 'role', 'target_location']

app = Flask(__name__)
users = Users()
services = {}

@app.route('/dispatcher/service', methods=['POST'])
def register_service():
    service = json.loads(request.get_json())
    name = service.pop('name')
    service['url'] = get_service_url(name)
    services[name] = service
    return 'NO_CONTENT', 204

@app.route('/dispatcher/inbox', methods=['POST'])
def inbox_new():
    msg = json.loads(request.get_json())

    user = users.get_user(msg['from']['id'])
    user['chat_id'] = msg['chat']['id']
    if (datetime.utcnow() - user['lastModified']).total_seconds() > 0.5*60:
      for field in PERISHABLE_FIELDS:
        user[field] = None

    reply = {}
    reply['chat_id'] = user['chat_id']
    reply['text'] = 'your request cannot be serviced'
    reply['keyboard'] = None

    if user.get('current_location', None) is None:
      if 'location' in msg.keys():
        user['current_location'] = msg['location']
        reply['text'] = 'do you want to ride or drive?'
        reply['keyboard'] = ['ride', 'drive']
      else:
        reply['text'] = 'please share your location'

    elif 'role' not in user.keys() or \
      user['role'] is None:
      if 'text' in msg.keys():
        if msg['text'] == 'ride':
          user['role'] = 'rider'
          reply['text'] = 'please share your destination'
        elif msg['text'] == 'drive':
          user['role'] = 'driver'
          reply['text'] = 'you are now in the waiting list'

    elif ('target_location' not in user.keys() or \
      user['target_location'] is None) and user['role'] == 'rider':
      if 'location' in msg.keys():
        user['target_location'] = msg['location']
        reply['text'] = 'looking for a driver'
      else:
        reply['text'] = 'please share your destination'

    users.update_user(user)
    print users.get_user(msg['from']['id'])

    send_message_telegram(reply)

    return 'OK'

if __name__ == '__main__':

    print 'starting ' + __file__ + '...'

    app.run(port=int(PORT), debug=True)
