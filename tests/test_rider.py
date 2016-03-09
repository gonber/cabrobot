import unittest
from services import utils
import requests
import json


class TestDriver(unittest.TestCase):
    def setUp(self):
        self.url = utils.get_service_url('rider')
        self.content = {'user': {},
                        'msg': {}
        }

    def test_looking_for_driver(self):
        self.content['user']['current_location'] = [0., 1.]
        self.content['user']['role'] = 'rider'
        self.content['user']['target_location'] = [1., 0.]
        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(200, r.status_code)

        reply_expected = {'user': {},
                          'text': 'looking for a driver'
        }
        self.assertEqual(reply_expected, r.json())

    def test_without_current_location(self):
        self.content['user']['role'] = 'rider'
        self.content['user']['target_location'] = [1., 0.]

        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(400, r.status_code)

    def test_without_target_location(self):
        self.content['user']['current_location'] = [0., 1.]
        self.content['user']['role'] = 'rider'

        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(400, r.status_code)

    def test_without_role_rider(self):
        self.content['user']['current_location'] = [0., 1.]
        self.content['user']['role'] = 'other'
        self.content['user']['target_location'] = [1., 0.]

        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(400, r.status_code)


if __name__ == "__main__":
    unittest.main()
