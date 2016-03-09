from utils import get_env_variable, get_service_url
from flask import Flask, request
import requests
import json

PORT = get_env_variable('DRIVER_PORT')

service = {
    'name': 'driver',
    'output_fields': ['available'],
    'input_fields': [['current_location', 'role']],
    'constraints': [{'role': 'driver'}]
}

app = Flask(__name__)

@app.route('/driver', methods=['POST'])
def driver():
    content = json.loads(request.json)
    user = content['user']
    msg = content['msg']

    reply = {'user': {},
             'text': ''
    }

    if user.get('role', None) != 'driver' or \
        user.get('current_location', None) is None:
        return 'BAD_REQUEST', 400
    else:
        if msg is {}:
            reply['user']['available'] = True
            reply['text'] = 'you are now in the waiting list'

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
