import unittest
from services import utils
import requests
import json


class TestLocator(unittest.TestCase):
    def setUp(self):
        self.url = utils.get_service_url('locator')
        self.content = {'user': {},
                        'msg': {}
        }

    def test_current_location_with_location(self):
        self.content['msg']['location'] = [0., 1.]
        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(200, r.status_code)

        reply_expected = {'user': {'current_location':[0.,1.]},
                          'text': ''
        }
        self.assertEqual(reply_expected, r.json())

    def test_current_location_without_location(self):
        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(200, r.status_code)

        reply_expected = {'user': {},
                          'text': 'please share your current location'
        }
        self.assertEqual(reply_expected, r.json())

    def test_target_location_with_location(self):
        self.content['user']['current_location'] = [0., 1.]
        self.content['user']['role'] = 'rider'
        self.content['msg']['location'] = [1., 2.]
        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(200, r.status_code)

        reply_expected = {'user': {'target_location':[1.,2.]},
                          'text': ''
        }
        self.assertEqual(reply_expected, r.json())


    def test_target_location_without_location(self):
        self.content['user']['current_location'] = [0., 1.]
        self.content['user']['role'] = 'rider'
        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(200, r.status_code)

        reply_expected = {'user': {},
                          'text': 'please share your target location'
        }
        self.assertEqual(reply_expected, r.json())


    def test_target_location_without_role_rider(self):
        self.content['user']['current_location'] = [0., 1.]
        self.content['user']['role'] = 'other'
        r = requests.post(self.url, json=json.dumps(self.content))
        self.assertEqual(400, r.status_code)


if __name__ == "__main__":
    unittest.main()
