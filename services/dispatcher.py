from utils import get_env_variable, get_service_url
from datetime import datetime
from flask import Flask, request
import requests
import json
from gateway_telegram import send_message_telegram
from users import Users

# rider_example = {
#   'lastModified': 'yesterday',
#   'current_location': 'here',
#   'role': 'rider',
#   'target_location': 'there',
#   'assigned_driver': 'notYet',
#   'proposed_driver': 'bob',
#   'valid': 'true',
#   'rejected_drivers': ['charles'],
#
#   'available': False,
#   'assigned_rider': 'notYey',
#   'proposed_rider': 'alice',
#   'rejected_riders': ['diane']
# }

PORT = get_env_variable('DISPATCHER_PORT')

PERISHABLE_FIELDS = ['current_location', 'role', 'target_location',
                     'available', 'proposed_driver']

app = Flask(__name__)
users = Users()
services = {}

@app.route('/dispatcher/service', methods=['POST'])
def register_service():
    service = json.loads(request.data)
    name = service.pop('name')
    service['url'] = get_service_url(name)
    services[name] = service
    return 'NO_CONTENT', 204

@app.route('/dispatcher/inbox', methods=['POST'])
def inbox_new():
    msg = json.loads(request.data)

    user = users.get_user(msg['from']['id'])
    user['chat_id'] = msg['chat']['id']
    if (datetime.utcnow() - user['lastModified']).total_seconds() > 0.5*60:
      for field in PERISHABLE_FIELDS:
        user[field] = None
    user.pop('lastModified')

    reply = {}
    reply['chat_id'] = user['chat_id']
    reply['text'] = 'your request cannot be serviced'
    reply['keyboard'] = None

    for _, service in services.iteritems():
        input_fields = service['input_fields']
        for i in range(len(input_fields)):
            output = service['output_fields'][i]
            fulfils = (user[output] is None)
            if fulfils:
                input_fields_per_output = input_fields[i]
                for field in input_fields_per_output:
                    if service['constraints'][i].get(field, None):
                        fulfils &= (user[field] ==
                          service['constraints'][i][field])
                    else:
                        fulfils &= (user[field] is not None)
            if fulfils:
                content = {'user': user,
                           'msg': msg
                }
                r = requests.post(service['url'], json=json.dumps(content))
                if r.status_code != 400:
                    reply = json.loads(r.json())
                    update_user = reply.pop('user')
                    update_user['_id'] = user['_id']
                    users.update_user(update_user)
                    if reply.get('text', '') != '':
                        send_message_telegram(reply)
                    return 'OK'

    return 'OK'

if __name__ == '__main__':

    print 'starting ' + __file__ + '...'

    app.run(port=int(PORT), debug=True)
