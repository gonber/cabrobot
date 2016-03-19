from services import driverqueue
from tests import test_stage
from tornado import gen
from tornado.testing import gen_test, main
from tornado.concurrent import Future
from unittest import mock


class TestDriverQueue(test_stage.TestStageBase):
    def setUp(self):
        super(TestDriverQueue, self).setUp()
        self.stage = driverqueue.DriverQueue(self.sender, self.users)
        self.stage.propagate = self.propagate

    @gen_test
    def test_drop_when_role_rider(self):
        user = {'role': 'rider'}

        yield self.stage.run(user, {})
        self.assertEqual(0, self.stage.propagate.call_count)
        self.assertEqual(0, self.stage.sender.call_count)

    @gen_test
    def test_dispatch(self):
        user = {'chat_id': 0}
        rider = {'username': 'noname'}

        yield self.stage.dispatch(user, rider)
        self.stage.sender.assert_called_with({
            'chat_id': user['chat_id'],
            'text': 'noname accepted your ride and is waiting for you.' + \
                ' text her if needed'
        })

    @gen_test
    def test_enquire(self):
        user = {'chat_id': 0}
        rider = {
            'current_location': [0., 0.],
            'target_location': [0., 1.]
        }
        msg = {'text': '666'}

        res = yield [
            self.stage.enquire(user, rider),
            self.stage.run(user, msg)
        ]

        self.assertEqual(666, res[0][0])
        self.assertEqual(None, res[0][1]['future'])
        self.stage.sender.assert_has_calls([
            mock.call({
                'text': 'request for a ride from:',
                'chat_id': 0
            }),
            mock.call({
                'location': [0.0, 0.0],
                'chat_id': 0
            }),
            mock.call({
                'text': 'to:',
                'chat_id': 0
            }),
            mock.call({
                'location': [0.0, 1.0],
                'chat_id': 0
            }),
            mock.call({
                'text': 'how much do you charge for it? (example answer: 25)',
                'chat_id': 0
            })
        ])

    @gen_test
    def test_enquire_timeout(self):
        user = {'chat_id': 0}
        rider = {
            'current_location': [0., 0.],
            'target_location': [0., 1.]
        }
        self.stage.enquire_timeout = 0.0001 # speedup test

        res = yield self.stage.enquire(user, rider)
        self.assertEqual(None, res)

    @gen_test
    def test_still_available_yes(self):
        user = {'chat_id': 0}
        msg = {'text': 'yes'}
        self.stage.renewal_period = 0.0001 # speedup test

        yield self.stage.run(user, msg)
        yield gen.sleep(0.001) # make sure callback is finished
        self.stage.sender.assert_has_calls([
            mock.call({
                'chat_id': user['chat_id'],
                'text': 'ok'
            }),
            mock.call({
                'chat_id': user['chat_id'],
                'text': 'are you still available to drive?',
                'keyboard': ['yes', 'no']
            })])

    @gen_test
    def test_still_available_no(self):
        msg = {'text': 'no'}

        yield self.stage.run({}, msg)
        self.assertEqual(0, self.stage.propagate.call_count)
        self.assertEqual(0, self.stage.sender.call_count)

    @gen_test
    def test_driver_queue(self):
        user = {'chat_id': 0}
        self.stage.renewal_period = 0.0001 # speedup test

        yield self.stage.run(user, {})
        yield gen.sleep(0.001) # make sure callback is finished
        self.stage.sender.assert_has_calls([
            mock.call({
                'chat_id': user['chat_id'],
                'text': 'you are now available'
            }),
            mock.call({
                'chat_id': user['chat_id'],
                'text': 'are you still available to drive?',
                'keyboard': ['yes', 'no']
            })])


if __name__ == "__main__":
    main()
