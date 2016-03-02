from utils import get_env_variable
from flask import Flask, request

LOCAL_API_TOKEN = get_env_variable('LOCAL_API_TOKEN')
HOST = get_env_variable('HOST') or '0.0.0.0'
PORT = get_env_variable('DISPATCHER_PORT') or get_env_variable('PORT')

app = Flask(__name__)

@app.route('/' + LOCAL_API_TOKEN + '/inbox', methods=['POST'])
def inbox_new():
    print 'inbox_new ' + request.data
    return 'OK'

if __name__ == '__main__':

    print 'starting ' + __file__ + '...'

    app.run(host=HOST, port=int(PORT), debug=True)
