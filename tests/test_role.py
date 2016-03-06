import unittest
from services import utils
import requests
import json


class TestRole(unittest.TestCase):
    def setUp(self):
        self.url = utils.get_service_url('role')
        self.content = {'user': {},
                        'msg': {}
        }

    def test_rider(self):
        self.content['user']['current_location'] = [0., 1.]
        self.content['msg']['text'] = 'ride'
        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(200, r.status_code)

        reply_expected = {'user': {'role': 'rider'},
                          'text': ''
        }
        self.assertEqual(reply_expected, r.json())

    def test_driver(self):
        self.content['user']['current_location'] = [0., 1.]
        self.content['msg']['text'] = 'drive'
        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(200, r.status_code)

        reply_expected = {'user': {'role': 'driver'},
                          'text': ''
        }
        self.assertEqual(reply_expected, r.json())

    def test_other(self):
        self.content['user']['current_location'] = [0., 1.]
        self.content['msg']['text'] = 'other'
        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(200, r.status_code)

        reply_expected = {'user': {},
                          'text': 'do you want to ride or drive?',
                          'keyboard': ['ride', 'drive']
        }
        self.assertEqual(reply_expected, r.json())

    def test_without_text(self):
        self.content['user']['current_location'] = [0., 1.]
        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(200, r.status_code)

        reply_expected = {'user': {},
                          'text': 'do you want to ride or drive?',
                          'keyboard': ['ride', 'drive']
        }
        self.assertEqual(reply_expected, r.json())

    def test_without_current_location(self):
        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(400, r.status_code)


if __name__ == "__main__":
    unittest.main()
