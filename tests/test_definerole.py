from services import definerole
from tests import test_stage
from tornado.testing import gen_test, main


class TestDefineRole(test_stage.TestStageBase):
    def setUp(self):
        super(TestDefineRole, self).setUp()
        self.stage = definerole.DefineRole(self.sender, self.users)
        self.stage.propagate = self.propagate

    @gen_test
    def test_set_rider(self):
        msg = {'text': 'ride'}

        yield self.stage.run({}, msg)
        self.propagate.assert_called_with({
            'role': 'rider'
        })

    @gen_test
    def test_set_driver(self):
        msg = {'text': 'drive'}

        yield self.stage.run({}, msg)
        self.propagate.assert_called_with({
            'role': 'driver'
        })

    @gen_test
    def test_ask_role(self):
        user = {'chat_id': 0}
        yield self.stage.run(user, {})
        self.stage.sender.assert_called_with({
            'chat_id': user['chat_id'],
            'text': 'do you want to ride or drive?',
            'keyboard': ['ride', 'drive']
        })


if __name__ == "__main__":
    main()
