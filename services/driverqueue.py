import stage
from tornado import gen, ioloop
from tornado.concurrent import Future
from datetime import timedelta


class DriverQueue(stage.Stage):
    def __init__(self, sender, users):
        super(DriverQueue, self).__init__(sender, users)
        self.renewal_period = 120
        self.enquire_timeout = 30

    @gen.coroutine
    def availability_timeout(self, user):
        yield self.sender({
              'chat_id': user['chat_id'],
              'text': 'are you still available to drive?',
              'keyboard': ['yes', 'no']
        })

    @gen.coroutine
    def availability_renew(self, user):
        yield self.persist(user, self.renewal_period)
        ioloop.IOLoop.current().call_later(0.9*self.renewal_period,
            self.availability_timeout, user)

    @gen.coroutine
    def enquire(self, user, rider):
        yield self.sender({
              'chat_id': user['chat_id'],
              'text': 'request for a ride from:'
        })
        yield self.sender({
              'chat_id': user['chat_id'],
              'location': rider['current_location']
        })
        yield self.sender({
              'chat_id': user['chat_id'],
              'text': 'to:'
        })
        yield self.sender({
              'chat_id': user['chat_id'],
              'location': rider['target_location']
        })
        yield self.sender({
              'chat_id': user['chat_id'],
              'text': 'how much do you charge for it? (example answer: 25)'
        })
        user['future'] = gen.with_timeout(
            timedelta(seconds=self.enquire_timeout), Future())
        yield self.persist(user)

        try:
            bid = yield user['future']
            return (bid, user)
        except:
            return (0, user)
        finally:
            user['future'] = None
            yield self.persist(user)

    @gen.coroutine
    def run(self, user, msg={}):
        if user.get('role') == 'rider':
            return
        if user.get('future'):
            try:
                bid = int(msg.get('text'))
                user['future'].set_result(bid)
            except:
                pass
        elif msg.get('text') == 'yes':
            yield self.sender({
                  'chat_id': user['chat_id'],
                  'text': 'ok'
            })
            yield self.availability_renew(user)
        elif msg.get('text') == 'no':
            pass
        else:
            yield self.sender({
                  'chat_id': user['chat_id'],
                  'text': 'you are now available'
            })
            yield self.availability_renew(user)
