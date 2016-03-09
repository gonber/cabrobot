from utils import get_env_variable, get_service_url
from flask import Flask, request
import requests
import json

PORT = get_env_variable('RIDER_PORT')

service = {
    'name': 'rider',
    'output_fields': ['proposed_driver'],
    'input_fields': [['current_location', 'role', 'target_location']],
    'constraints': [{'role': 'rider'}]
}

app = Flask(__name__)

@app.route('/rider', methods=['POST'])
def driver():
    content = json.loads(request.json)
    user = content['user']
    msg = content['msg']

    reply = {'user': {},
             'text': ''
    }

    if user.get('role', None) != 'rider' or \
         user.get('current_location', None) is None or \
         user.get('target_location', None) is None:
        return 'BAD_REQUEST', 400
    else:
        if msg == {}:
            reply['text'] = 'looking for a driver'

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
