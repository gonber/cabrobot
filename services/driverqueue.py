import stage
from tornado import gen, ioloop


class DriverQueue(stage.Stage):
    def __init__(self, sender, users):
        super(DriverQueue, self).__init__(sender, users)
        self.timeout_in_seconds = 120

    @gen.coroutine
    def availability_timeout(self, user):
        yield gen.sleep(0.9*self.timeout_in_seconds)
        yield self.sender({
                  'chat_id': user['chat_id'],
                  'text': 'are you still available to drive?',
                  'keyboard': ['yes', 'no']
              })

    @gen.coroutine
    def availability_renew(self, user):
        yield self.persist(user, self.timeout_in_seconds)
        ioloop.IOLoop.current().add_callback(self.availability_timeout, user)

    @gen.coroutine
    def run(self, user, msg={}):
        if user.get('role') == 'rider':
            return
        if msg.get('text') == 'yes':
            yield self.sender({
                  'chat_id': user['chat_id'],
                  'text': 'ok'
            })
            yield self.availability_renew(user)
        elif msg.get('text') == 'no':
            return
        else:
            yield self.sender({
                  'chat_id': user['chat_id'],
                  'text': 'you are now available'
            })
            yield self.availability_renew(user)
