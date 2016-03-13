from tornado import gen, ioloop
from datetime import datetime, timedelta


class Stage():
    def __init__(self, sender, users):
        self.sender = sender
        self.users = users
        self.next_stages = []

    @gen.coroutine
    def report_error(self, user):
        yield self.sender({
            'chat_id': user['chat_id'],
            'text': 'request could not be fulfiled'
        })

    @gen.coroutine
    def persist(self, user, expires_in_seconds):
        user['stage'] = type(self).__name__
        user['expires'] = datetime.utcnow() + \
                          timedelta(0, expires_in_seconds)
        yield self.users.update_user(user)

    @gen.coroutine
    def propagate(self, user, msg={}):
        for next in self.next_stages:
            ioloop.IOLoop.current() \
            .spawn_callback(next(self.sender, self.users).run, user, msg)
