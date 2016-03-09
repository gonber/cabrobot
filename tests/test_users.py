import unittest
import mock
from services import users
from datetime import datetime


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.users = users.Users()
        self.users.drop()

    def test_get_user_new(self):
        user = self.users.get_user(200)

        expected_user = {
            'last_modified': datetime(1989, 8, 24),
             '_id': 200
        }

        self.assertEqual(expected_user, user)

    def test_update_user(self):
        user = self.users.get_user(200)
        user['new_field'] = 1
        self.users.update_user(user)

        user = self.users.get_user(200)

        self.assertEqual(1, user['new_field'])
        self.assertTrue((datetime.utcnow() - user['last_modified'])
            .total_seconds() < 10)


if __name__ == "__main__":
    unittest.main()
