from services import locateorigin
from tests import test_stage
from tornado.testing import gen_test, main


class TestLocateOrigin(test_stage.TestStageBase):
    def setUp(self):
        super(TestLocateOrigin, self).setUp()
        self.stage = locateorigin.LocateOrigin(self.sender, self.users)
        self.stage.propagate = self.propagate

    @gen_test
    def test_set_current_location(self):
        msg = {'location': [0., 0.]}

        yield self.stage.run({}, msg)
        self.propagate.assert_called_with({
            'current_location': msg['location']
        })

    @gen_test
    def test_ask_current_location(self):
        user = {'chat_id': 0}
        yield self.stage.run(user)
        self.stage.sender.assert_called_with({
            'chat_id': user['chat_id'],
            'text': 'please share your current location'
        })


if __name__ == "__main__":
    main()
