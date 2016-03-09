from utils import get_env_variable, get_service_url
from flask import Flask, request
import requests
import json

PORT = get_env_variable('ROLE_PORT')

service = {
    'name': 'role',
    'output_fields': ['role'],
    'input_fields': [['current_location']],
    'constraints': [{}]
}

app = Flask(__name__)

@app.route('/role', methods=['POST'])
def role():
    content = json.loads(request.json)
    user = content['user']
    msg = content['msg']

    reply = {'user': {},
             'text': ''
    }

    if user.get('role', None) is None and \
         user.get('current_location', None) is not None:
        if msg.get('text', None) == 'ride':
            reply['user']['role'] = 'rider'
        elif msg.get('text', None) == 'drive':
            reply['user']['role'] = 'driver'
        else:
            reply['text'] = 'do you want to ride or drive?'
            reply['keyboard'] = ['ride', 'drive']
    else:
        return 'BAD_REQUEST', 400

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
