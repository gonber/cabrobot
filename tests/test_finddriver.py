from services import finddriver
from tests import test_stage
from tornado.testing import gen_test, main


class TestFindDriver(test_stage.TestStageBase):
    def setUp(self):
        super(TestFindDriver, self).setUp()
        self.stage = finddriver.FindDriver(self.sender, self.users)
        self.stage.propagate = self.propagate

    @gen_test
    def test_find_driver(self):
        user = {'chat_id': 0}

        yield self.stage.run(user, {})
        self.stage.sender.assert_called_with({
            'chat_id': user['chat_id'],
            'text': 'found driver 60 sec later'
        })


if __name__ == "__main__":
    main()
