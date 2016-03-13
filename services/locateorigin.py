import stage, definerole
from tornado import gen


class LocateOrigin(stage.Stage):
    def __init__(self, sender, users):
        super(LocateOrigin, self).__init__(sender, users)
        self.next_stages.append(definerole.DefineRole)

    @gen.coroutine
    def run(self, user, msg={}):
        if msg.get('location'):
            user['current_location'] = msg['location']
            yield self.propagate(user)
        else:
            yield self.sender({
                'chat_id': user['chat_id'],
                'text': 'please share your current location'
            })
            yield self.persist(user, 30)
