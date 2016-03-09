import unittest
import mock
from services import dispatcher, driver, locator, rider, role, utils
import requests
import requests_mock
import json
import copy


class TestDispatcher(unittest.TestCase):
    def dispatcher_calls_service(self, service, mock_request):
        r = self.app.post('/dispatcher/service', data=json.dumps(service))
        self.assertEqual(204, r.status_code)

        dispatcher.users.update_user(self.user)

        msg = {'from': {'id': 0},
               'chat': {'id': 0}
        }
        self.user.pop('lastModified', None)
        reply = {'user': self.user,
                 'text': 'a reply'
        }

        mock_request.post(utils.get_service_url(service['name']),
            json=json.dumps(reply))
        self.app.post('/dispatcher/inbox', data=json.dumps(msg))

    def setUp(self):
        dispatcher.send_message_telegram = mock.MagicMock()

        self.app = dispatcher.app.test_client()
        self.user = dispatcher.users.get_user(0)
        for field in dispatcher.PERISHABLE_FIELDS:
            self.user[field] = None

    def test_register_service(self):
        service = copy.copy(role.service)
        r = self.app.post('/dispatcher/service', data=json.dumps(service))
        self.assertEqual(204, r.status_code)

        name = service.pop('name')
        service['url'] = utils.get_service_url(name)
        self.assertEqual(dispatcher.services[name], service)

    @requests_mock.Mocker()
    def test_locator_current_location_dispatch(self, m):
        self.dispatcher_calls_service(locator.service, m)

        self.assertEqual(1, m.call_count)
        self.assertTrue(dispatcher.send_message_telegram.called)

    @requests_mock.Mocker()
    def test_locator_target_location_dispatch(self, m):
        self.user['current_location'] = 'here'
        self.user['role'] = 'rider'

        self.dispatcher_calls_service(locator.service, m)

        self.assertEqual(1, m.call_count)
        self.assertTrue(dispatcher.send_message_telegram.called)

    @requests_mock.Mocker()
    def test_locator_target_location_dispatch_negative(self, m):
        self.user['current_location'] = 'here'
        self.user['role'] = 'other'

        self.dispatcher_calls_service(locator.service, m)

        self.assertEqual(0, m.call_count)
        self.assertFalse(dispatcher.send_message_telegram.called)

    @requests_mock.Mocker()
    def test_role_dispatch(self, m):
        self.user['current_location'] = 'here'

        self.dispatcher_calls_service(role.service, m)

        self.assertEqual(1, m.call_count)
        self.assertTrue(dispatcher.send_message_telegram.called)

    @requests_mock.Mocker()
    def test_rider_dispatch(self, m):
        self.user['current_location'] = 'here'
        self.user['role'] = 'rider'
        self.user['target_location'] = 'here'

        self.dispatcher_calls_service(rider.service, m)

        self.assertEqual(1, m.call_count)
        self.assertTrue(dispatcher.send_message_telegram.called)

    @requests_mock.Mocker()
    def test_driver_dispatch(self, m):
        self.user['current_location'] = 'here'
        self.user['role'] = 'driver'

        self.dispatcher_calls_service(driver.service, m)

        self.assertEqual(1, m.call_count)
        self.assertTrue(dispatcher.send_message_telegram.called)

    @requests_mock.Mocker()
    def test_driver_dispatch_negative(self, m):
        self.dispatcher_calls_service(driver.service, m)

        self.assertEqual(0, m.call_count)
        self.assertFalse(dispatcher.send_message_telegram.called)


if __name__ == "__main__":
    unittest.main()
