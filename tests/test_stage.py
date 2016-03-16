from services import stage
from tornado import gen
from tornado.testing import AsyncTestCase, gen_test, main
from tornado.concurrent import Future
from unittest import mock


class TestStageBase(AsyncTestCase):
    def setUp(self):
        super(TestStageBase, self).setUp()
        self.future = Future()
        self.future.set_result(True)

        self.propagate = mock.MagicMock(return_value=self.future)
        self.sender = mock.MagicMock(return_value=self.future)

        self.users = mock.Mock()
        self.users.update_user = mock.MagicMock(return_value=self.future)


class TestStage(TestStageBase):
    def setUp(self):
        super(TestStage, self).setUp()
        self.stage = stage.Stage(self.sender, self.users)

    @gen_test
    def test_report_error(self):
        user = {'chat_id': 0}
        yield self.stage.report_error(user)
        self.sender.assert_called_with({
            'chat_id': user['chat_id'],
            'text': 'request could not be fulfiled'
        })

    @gen_test
    def test_persist_with_expiration(self):
        yield self.stage.persist({}, 1)
        call_arg = self.users.update_user.call_args[0][0]
        self.assertTrue(call_arg.get('expires'))
        self.assertEqual('Stage', call_arg.get('stage'))

    @gen_test
    def test_persist_without_expiration(self):
        yield self.stage.persist({})
        call_arg = self.users.update_user.call_args[0][0]
        self.assertEqual(None, call_arg.get('expires'))
        self.assertEqual('Stage', call_arg.get('stage'))

    @gen_test
    def test_propagate(self):
        runMock = mock.MagicMock(return_value=self.future)
        stageMock = mock.Mock()
        stageMock.run = runMock
        nextMock = mock.MagicMock(return_value=stageMock)

        self.stage.next_stages.append(nextMock)
        yield self.stage.propagate({})
        yield gen.moment # make sure callback is finished
        self.assertEqual(1, runMock.call_count)

if __name__ == "__main__":
    main()
