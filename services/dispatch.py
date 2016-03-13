import stage, users
from locateorigin import LocateOrigin
from definerole import DefineRole
from locatetarget import LocateTarget
from finddriver import FindDriver
from datetime import datetime
from tornado import gen, ioloop

g_users = users.Users()

class Dispatch(stage.Stage):
    def __init__(self, sender):
        super(Dispatch, self).__init__(sender, g_users)
        self.next_stages.append(LocateOrigin)

    @gen.coroutine
    def run(self, msg):
        user = self.users.get_user(msg['from']['id'])
        user['chat_id'] = msg['chat']['id']
        if user.get('stage') and \
           (user.get('expires') - datetime.utcnow()).total_seconds() > 0:
            ioloop.IOLoop.current() \
            .spawn_callback(eval(user['stage'])(self.sender, self.users).run,
                            user, msg)
        else:
            yield self.propagate(user, msg)
