from services import dispatch
from tests import test_stage
from tornado import gen
from tornado.testing import gen_test, main
from tornado.concurrent import Future
from datetime import datetime, timedelta
from unittest import mock


class TestDispatch(test_stage.TestStageBase):
    def setUp(self):
        super(TestDispatch, self).setUp()
        self.stage = dispatch.Dispatch(self.sender, self.users)
        self.stage.propagate = self.propagate

        self.future_get_user = Future()
        self.users.get_user = mock.MagicMock(return_value=self.future_get_user)

    @gen_test
    def test_fastforward_to_stage(self):
        msg = {
            'from': {'id': 0},
            'chat': {'id': 0}
        }
        user = {
            'stage': 'FindDriver',
            'expires': datetime.utcnow() + timedelta(0,100)
        }
        self.future_get_user.set_result(user)

        runMock = mock.MagicMock(return_value=self.future)
        stageMock = mock.Mock()
        stageMock.run = runMock
        dispatch.FindDriver = mock.MagicMock(return_value=stageMock)

        yield self.stage.run(msg)
        yield gen.sleep(0.001) # make sure spawn callback is finished
        self.assertEqual(1, runMock.call_count)
        self.assertEqual(0, self.propagate.call_count)

    @gen_test
    def test_expired_stage(self):
        msg = {
            'from': {'id': 0},
            'chat': {'id': 0}
        }
        user = {
            'stage': 'FindDriver',
            'expires': datetime.utcnow() - timedelta(0,100)
        }
        self.future_get_user.set_result(user)

        runMock = mock.MagicMock(return_value=self.future)
        stageMock = mock.Mock()
        stageMock.run = runMock
        dispatch.FindDriver = mock.MagicMock(return_value=stageMock)

        yield self.stage.run(msg)
        yield gen.sleep(0.001) # make sure spawn callback is finished
        self.assertEqual(0, runMock.call_count)
        self.assertEqual(1, self.propagate.call_count)

    @gen_test
    def test_startup(self):
        msg = {
            'from': {'id': 0},
            'chat': {'id': 0}
        }
        self.future_get_user.set_result({})

        yield self.stage.run(msg)
        self.propagate.assert_called_with({
            'chat_id': msg['chat']['id'],
        }, msg)

if __name__ == "__main__":
    main()
