import utils
import dispatch
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
    yield bot.sendMessage(msg['chat_id'], msg['text'], reply_markup=keyboard)


if __name__ == '__main__':

    @asyncio.coroutine
    def handle(msg):
        yield from to_asyncio_future(
            dispatch.Dispatch(send_message_telegram).run(msg)
        )

    AsyncIOMainLoop().install()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.messageLoop(handle))
    loop.run_forever()
