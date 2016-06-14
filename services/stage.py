from tornado import gen, ioloop
from datetime import datetime, timedelta


class Stage():
    def __init__(self, sender, users):
        self.sender = sender
        self.users = users
        self.next_stages = []
        self.user_interaction_timeout = 60

    @gen.coroutine
    def report_error(self, user):
        yield self.sender({
            'chat_id': user['chat_id'],
            'text': 'request could not be fulfiled'
        })

    @gen.coroutine
    def persist(self, user, expires_in_seconds=0):
        user['stage'] = type(self).__name__
        if expires_in_seconds:
            user['expires'] = datetime.utcnow() + \
                              timedelta(0, expires_in_seconds)
        yield self.users.update_user(user)

    @gen.coroutine
    def propagate(self, user, msg={}):
        for next in self.next_stages:
            ioloop.IOLoop.current() \
            .add_callback(next(self.sender, self.users).run, user, msg)
