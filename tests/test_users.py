from services import users
from tornado.testing import AsyncTestCase, gen_test, main
from datetime import datetime


class TestUsers(AsyncTestCase):
    def setUp(self):
        super(TestUsers, self).setUp()
        self.users = users.Users()
        self.users.drop()

    @gen_test
    def test_get_user_new(self):
        user = yield self.users.get_user(200)

        expected_user = {
            'last_modified': datetime(1989, 8, 24),
             '_id': 200
        }

        self.assertEqual(expected_user, user)

    @gen_test
    def test_update_user(self):
        user = yield self.users.get_user(200)
        user['new_field'] = 1
        yield self.users.update_user(user)

        user = yield self.users.get_user(200)

        self.assertEqual(1, user['new_field'])
        self.assertTrue((datetime.utcnow() - user['last_modified'])
            .total_seconds() < 10)


if __name__ == "__main__":
    main()
