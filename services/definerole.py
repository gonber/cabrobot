import stage, locatetarget
from tornado import gen


class DefineRole(stage.Stage):
    def __init__(self, sender, users):
        super(DefineRole, self).__init__(sender, users)
        self.next_stages.append(locatetarget.LocateTarget)

    @gen.coroutine
    def run(self, user, msg={}):
        if msg.get('text') == 'ride':
            user['role'] = 'rider'
            yield self.propagate(user)
        elif msg.get('text') == 'drive':
            user['role'] = 'driver'
            yield self.propagate(user)
        else:
            yield self.sender({
                'chat_id': user['chat_id'],
                'text': 'do you want to ride or drive?',
                'keyboard': ['ride', 'drive']
            })
            yield self.persist(user, 30)
