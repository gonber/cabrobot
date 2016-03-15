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
    def test_still_available_yes(self):
        user = {'chat_id': 0}
        msg = {'text': 'yes'}
        self.stage.timeout_in_seconds = 0.0001 # speedup test

        yield self.stage.run(user, msg)
        yield gen.sleep(0.001) # make sure spawn callback is finished
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
        self.stage.timeout_in_seconds = 0.0001 # speedup test

        yield self.stage.run(user, {})
        yield gen.sleep(0.001) # make sure spawn callback is finished
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
