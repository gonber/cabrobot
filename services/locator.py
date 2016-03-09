from utils import get_env_variable, get_service_url
from flask import Flask, request
import requests
import json

PORT = get_env_variable('LOCATOR_PORT')

service = {
    'name': 'locator',
    'output_fields': ['current_location', 'target_location'],
    'input_fields': [[], ['current_location', 'role']],
    'constraints': [{}, {'role': 'rider'}]
}

app = Flask(__name__)

@app.route('/locator', methods=['POST'])
def locator():
    content = json.loads(request.json)
    user = content['user']
    msg = content['msg']

    reply = {'user': {},
             'text': ''
    }

    if user.get('current_location', None) is None:
        if msg.get('location', None):
            reply['user']['current_location'] = msg['location']
        else:
            reply['text'] = 'please share your current location'
    elif user.get('target_location', None) is None:
        if user.get('role', None) != 'rider':
             return 'BAD_REQUEST', 400
        elif msg.get('location', None):
            reply['user']['target_location'] = msg['location']
        else:
            reply['text'] = 'please share your target location'

    return json.dumps(reply), 200


if __name__ == '__main__':

    print 'starting ' + __file__ + '...'

    r = requests.post(
      "{}/{}".format(get_service_url('dispatcher'), 'service'),
      data=json.dumps(service))
    if r.status_code != 204:
        print __file__ + ': service was not properly registered and is' \
          + ' not callable'

    app.run(port=int(PORT), debug=True)
