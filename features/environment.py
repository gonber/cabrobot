import sys
sys.path.append('services/')
from services import users, dispatch
from tornado.gen import moment
from tornado.ioloop import IOLoop
from tornado.concurrent import Future
from tornado.testing import AsyncTestCase, gen_test
from unittest import mock


class TestUser(AsyncTestCase):
    def __init__(self, context, username, in_id):
        self.io_loop = IOLoop.current()
        self.send_message = context.send_message
        self.users = context.users
        self.username = username
        self.user_id = in_id
        self.msg = {
            'from': {
                'id': self.user_id,
                'username': self.username
            },
            'chat': {
                'id': self.user_id
            }
        }

    def writes(self, text):
        self.msg.pop('location', None)
        self.msg['text'] = text
        self._send()
        return self

    def location(self, latitude, longitude):
        self.msg.pop('text', None)
        self.msg['location'] = {
            'latitude': latitude,
            'longitude': longitude
        }
        self._send()
        return self

    @gen_test
    def _send(self):
        yield dispatch.Dispatch(self.send_message, self.users).run(self.msg)

    def reads(self, text):
        call_arg = self.send_message.call_args[0][0]
        self.assertTrue(self.user_id == call_arg.get('chat_id'))
        self.assertTrue(text == call_arg.get('text'))
        return self

    @gen_test(timeout=600)
    def wait_new_message(self):
        base = self.send_message.call_count
        while self.send_message.call_count <= base:
            yield moment
        return self

def before_scenario(context, scenario):
    future = Future()
    future.set_result(True)
    context.send_message = mock.MagicMock(return_value=future)
    context.users = users.Users()
    context.users.drop()

    context.bob = TestUser(context, 'bob', '101')
