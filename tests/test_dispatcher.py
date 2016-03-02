import unittest
import requests


class TestDispatcher(unittest.TestCase):
    def setUp(self):
        self.url = "http://127.0.0.1:5000/dispatcher"

    def test_inbox(self):
        """ Test /dispatch/inbox"""

        reply = requests.post("{}/{}".format(self.url, 'inbox'))
        print reply


if __name__ == "__main__":
    unittest.main()
