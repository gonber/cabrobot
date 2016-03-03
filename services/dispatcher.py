from utils import get_env_variable
from flask import Flask, request

PORT = get_env_variable('DISPATCHER_PORT')

app = Flask(__name__)

@app.route('/dispatcher/inbox', methods=['POST'])
def inbox_new():
    print 'inbox_new ' + request.data
    return 'OK'

if __name__ == '__main__':

    print 'starting ' + __file__ + '...'

    app.run(port=int(PORT), debug=True)
