import sys
sys.path.append('services/')
from services import users, dispatch
from tornado.gen import moment
from tornado.ioloop import IOLoop
from tornado.concurrent import Future
from tornado.testing import AsyncTestCase, gen_test
from unittest import mock


class TestUser(AsyncTestCase):
    def __init__(self, context, username, user_id):
        self.io_loop = IOLoop.current()

        self.send_message = context.send_message
        self.users = context.users

        self.username = username
        self.user_id = user_id
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

    @gen_test(timeout=20)
    def reads(self, text):
        while True:
            for call in self.send_message.call_args_list:
                msg = call[0][0]
                if msg['chat_id'] == self.user_id:
                    if msg.get('text') == text:
                        self.send_message.call_args_list.remove(call)
                        return self
                    else:
                        print(msg.get('text'))
                        self.assertTrue(False)
            yield moment

    @gen_test(timeout=20)
    def receives_location(self):
        while True:
            for call in self.send_message.call_args_list:
                msg = call[0][0]
                if msg['chat_id'] == self.user_id:
                    if msg.get('location'):
                        self.send_message.call_args_list.remove(call)
                        return self
                    else:
                        self.assertTrue(False)
            yield moment

    def clear_inbox(self):
        for call in self.send_message.call_args_list:
            msg = call[0][0]
            if msg['chat_id'] == self.user_id:
                self.send_message.call_args_list.remove(call)

        return self


def before_scenario(context, scenario):
    future = Future()
    future.set_result(True)
    context.send_message = mock.MagicMock(return_value=future)

    context.users = users.Users()
    context.users.drop()

    context.test_users = {}
