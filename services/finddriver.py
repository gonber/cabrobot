import stage, driverqueue
from tornado import gen


class FindDriver(stage.Stage):
    def __init__(self, sender, users):
        super(FindDriver, self).__init__(sender, users)
        self.dq = driverqueue.DriverQueue(self.sender, self.users)
        self.driver_search_radius = 2000

    @gen.coroutine
    def run(self, user, msg={}):
        if msg.get('text') == 'accept':
            yield self.sender({
                  'chat_id': user['chat_id'],
                  'text': 'driver is on her way. text her if needed'
            })
            yield self.dq.dispatch(user['proposed_driver'], user)
            user['proposed_driver'] = None
            yield self.persist(user)
        elif msg.get('text') == 'reject':
            user['proposed_driver'] = None
            yield self.persist(user)
        else:
            yield self.sender({
                'chat_id': user['chat_id'],
                'text': 'looking for a driver'
            })

            drivers = yield self.users.get_drivers_within_distance(
                user['current_location'], self.driver_search_radius)

            responses = yield [
                          self.dq.enquire(driver, user) for driver in drivers]
            responses = [response for response in responses
                            if response is not None]

            if len(responses) > 0:
                responses.sort(key=lambda tup: tup[0])
                bid = responses[0][0]
                driver = responses[0][1]

                yield self.sender({
                    'chat_id': user['chat_id'],
                    'text': driver['username'] + ' will take you there for ' \
                        + str(bid),
                    'keyboard': ['accept', 'reject']
                })
                user['proposed_driver'] = driver
                yield self.persist(user, self.user_interaction_timeout)
            else:
                yield self.sender({
                    'chat_id': user['chat_id'],
                    'text': 'no available drivers found'
                })
                user['proposed_driver'] = None
