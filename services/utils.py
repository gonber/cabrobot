import os
from os.path import join, dirname
from dotenv import load_dotenv


def get_env_variable(name):
    try:
        value = os.environ[name]
    except:
        # Is there an .env file?
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        value = os.environ.get(name)

    return value

def get_service_url(name):
    return 'http://localhost:' + get_env_variable(name.upper() +'_PORT') \
         + '/' + name
