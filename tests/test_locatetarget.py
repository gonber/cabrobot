from services import locatetarget
from tests import test_stage
from tornado.testing import gen_test, main


class TestLocateTarget(test_stage.TestStageBase):
    def setUp(self):
        super(TestLocateTarget, self).setUp()
        self.stage = locatetarget.LocateTarget(self.sender, self.users)
        self.stage.propagate = self.propagate

    @gen_test
    def test_set_target_location(self):
        msg = {'location': [0., 0.]}

        yield self.stage.run({}, msg)
        self.propagate.assert_called_with({
            'target_location': msg['location']
        })

    @gen_test
    def test_drop_when_role_driver(self):
        user = {'role': 'driver'}

        yield self.stage.run(user, {})
        self.assertEqual(0, self.stage.propagate.call_count)
        self.assertEqual(0, self.stage.sender.call_count)

    @gen_test
    def test_ask_target_location(self):
        user = {
            'chat_id': 0,
            'role': 'rider'
        }
        yield self.stage.run(user, {})
        self.stage.sender.assert_called_with({
            'chat_id': user['chat_id'],
            'text': 'please share your target location'
        })


if __name__ == "__main__":
    main()
