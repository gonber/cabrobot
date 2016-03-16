import stage
from tornado import gen


class FindDriver(stage.Stage):
    def __init__(self, sender, users):
        super(FindDriver, self).__init__(sender, users)

    @gen.coroutine
    def run(self, user, msg={}):
        yield self.sender({
            'chat_id': user['chat_id'],
            'text': 'found driver 60 sec later'
        })
        yield self.persist(user, 30)
