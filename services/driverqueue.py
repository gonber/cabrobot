import stage
from tornado import gen, ioloop
from tornado.concurrent import Future
from datetime import timedelta


class DriverQueue(stage.Stage):
    futures = {}

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
    def dispatch(self, user, rider):
        yield self.sender({
            'chat_id': user['chat_id'],
            'text': rider['username'] + ' accepted your ride and is' + \
                ' waiting for you. text her if needed'
        })

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
        DriverQueue.futures[user['chat_id']] = gen.with_timeout(
            timedelta(seconds=self.enquire_timeout), Future())

        try:
            bid = yield DriverQueue.futures[user['chat_id']]
            return (bid, user)
        except:
            pass
        finally:
            DriverQueue.futures.pop(user['chat_id'])

    @gen.coroutine
    def run(self, user, msg={}):
        if user.get('role') == 'rider':
            return
        if DriverQueue.futures.get(user['chat_id']):
            try:
                bid = int(msg.get('text'))
                DriverQueue.futures[user['chat_id']].set_result(bid)
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
