from services import finddriver
from tests import test_stage
from tornado import gen
from tornado.testing import gen_test, main
from tornado.concurrent import Future
from unittest import mock


class TestFindDriver(test_stage.TestStageBase):
    def setUp(self):
        super(TestFindDriver, self).setUp()

        self.stage = finddriver.FindDriver(self.sender, self.users)
        self.stage.propagate = self.propagate

        self.stage.dq = mock.Mock()

    @gen_test
    def test_accept_driver(self):
        user = {
            'chat_id': 0,
            'proposed_driver': 'mydriver'}
        msg = {'text': 'accept'}

        self.stage.dq.dispatch = mock.MagicMock(return_value=self.future)

        yield self.stage.run(user, msg)
        self.stage.sender.assert_called_with({
            'chat_id': user['chat_id'],
            'text': 'driver is on her way. text her if needed'
        })
        self.stage.dq.dispatch.assert_called_with('mydriver', user)
        self.assertEqual(None, user['proposed_driver'])

    @gen_test
    def test_reject_driver(self):
        user = {'proposed_driver': 'mydriver'}
        msg = {'text': 'reject'}

        self.stage.dq.dispatch = mock.MagicMock(return_value=self.future)

        yield self.stage.run(user, msg)
        self.assertEqual(0, self.stage.sender.call_count)
        self.assertEqual(0, self.stage.dq.dispatch.call_count)
        self.assertEqual(None, user['proposed_driver'])

    @gen_test
    def test_looking_for_driver(self):
        user = {
            'chat_id': 0,
            'current_location': [0., 0.]
        }

        drivers = [
            {'username': 'driver0'},
            {'username': 'driver1'},
            {'username': 'driver2'},
        ]
        future_get_drivers = Future()
        future_get_drivers.set_result(drivers)
        self.users.get_drivers_within_distance = mock.MagicMock(
            return_value=future_get_drivers
        )

        futures_enquire = [Future() for i in range(len(drivers))]
        futures_enquire[0].set_result(None)
        futures_enquire[1].set_result((10, drivers[1]))
        futures_enquire[2].set_result((20, drivers[2]))
        self.stage.dq.enquire = mock.MagicMock()
        self.stage.dq.enquire.side_effect = futures_enquire

        yield self.stage.run(user, {})

        self.stage.sender.assert_has_calls([
            mock.call({
                'chat_id': 0,
                'text': 'looking for a driver'
            }),
            mock.call({
                'chat_id': 0,
                'text': 'driver1 will take you there for 10',
                'keyboard': ['accept', 'reject']
            })
        ])
        self.assertEqual(2,self.stage.sender.call_count)
        self.assertEqual('driver1', user['proposed_driver']['username'])

    @gen_test
    def test_looking_for_driver_no_response(self):
        user = {
            'chat_id': 0,
            'current_location': [0., 0.]
        }

        drivers = [
            {'username': 'driver0'},
            {'username': 'driver1'},
            {'username': 'driver2'},
        ]
        future_get_drivers = Future()
        future_get_drivers.set_result(drivers)
        self.users.get_drivers_within_distance = mock.MagicMock(
            return_value=future_get_drivers
        )

        futures_enquire = [Future() for i in range(len(drivers))]
        futures_enquire[0].set_result(None)
        futures_enquire[1].set_result(None)
        futures_enquire[2].set_result(None)
        self.stage.dq.enquire = mock.MagicMock()
        self.stage.dq.enquire.side_effect = futures_enquire

        yield self.stage.run(user, {})

        self.stage.sender.assert_has_calls([
            mock.call({
                'chat_id': 0,
                'text': 'looking for a driver'
            }),
            mock.call({
                'chat_id': 0,
                'text': 'no available drivers found'
            })
        ])
        self.assertEqual(2,self.stage.sender.call_count)
        self.assertEqual(None, user['proposed_driver'])

    @gen_test
    def test_looking_for_driver_no_drivers(self):
        user = {
            'chat_id': 0,
            'current_location': [0., 0.]
        }

        drivers = []
        future_get_drivers = Future()
        future_get_drivers.set_result(drivers)
        self.users.get_drivers_within_distance = mock.MagicMock(
            return_value=future_get_drivers
        )

        yield self.stage.run(user, {})

        self.stage.sender.assert_has_calls([
            mock.call({
                'chat_id': 0,
                'text': 'looking for a driver'
            }),
            mock.call({
                'chat_id': 0,
                'text': 'no available drivers found'
            })
        ])
        self.assertEqual(2,self.stage.sender.call_count)
        self.assertEqual(None, user['proposed_driver'])


if __name__ == "__main__":
    main()
