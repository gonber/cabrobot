import stage, finddriver
from tornado import gen


class LocateTarget(stage.Stage):
    def __init__(self, sender, users):
        super(LocateTarget, self).__init__(sender, users)
        self.next_stages.append(finddriver.FindDriver)

    @gen.coroutine
    def run(self, user, msg={}):
        if user.get('role') == 'driver':
            return
        if msg.get('location'):
            user['target_location'] = msg['location']
            yield self.propagate(user)
        else:
            yield self.sender({
                      'chat_id': user['chat_id'],
                      'text': 'please share your target location'
                  })
            yield self.persist(user, 30)
