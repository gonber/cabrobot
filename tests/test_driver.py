import unittest
from services import utils
import requests
import json


class TestDriver(unittest.TestCase):
    def setUp(self):
        self.url = utils.get_service_url('driver')
        self.content = {'user': {},
                        'msg': {}
        }

    def test_waiting_list(self):
        self.content['user']['current_location'] = [0., 1.]
        self.content['user']['role'] = 'driver'
        self.content['msg'] = None
        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(200, r.status_code)

        reply_expected = {'user': {'available': True},
                          'text': 'you are now in the waiting list'
        }
        self.assertEqual(reply_expected, r.json())

    def test_without_current_location(self):
        self.content['user']['role'] = 'driver'

        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(400, r.status_code)

    def test_without_role_driver(self):
        self.content['user']['current_location'] = [0., 1.]
        self.content['user']['role'] = 'other'

        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(400, r.status_code)


if __name__ == "__main__":
    unittest.main()
