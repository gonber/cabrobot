import utils
import users, dispatch
from tornado.platform.asyncio import to_asyncio_future, AsyncIOMainLoop
import telepot.async
import asyncio


TELEGRAM_API_TOKEN = utils.get_env_variable('TELEGRAM_API_TOKEN')

bot = telepot.async.Bot(TELEGRAM_API_TOKEN)

@asyncio.coroutine
def send_message_telegram(msg):
    keyboard = None
    if msg.get('keyboard'):
      keyboard = {'keyboard': [msg['keyboard']],
                  'one_time_keyboard': True,
                  'resize_keyboard': True}
    if msg.get('text'):
        yield bot.sendMessage(msg['chat_id'], msg['text'],
            reply_markup=keyboard)
    elif msg.get('location'):
        yield bot.sendLocation(msg['chat_id'],
            longitude=msg['location']['longitude'],
            latitude=msg['location']['latitude'],
            reply_markup=keyboard)


if __name__ == '__main__':

    @asyncio.coroutine
    def handle(msg):
        yield from to_asyncio_future(
            dispatch.Dispatch(send_message_telegram, g_users).run(msg)
        )

    AsyncIOMainLoop().install()

    g_users = users.Users()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.messageLoop(handle))
    loop.run_forever()
