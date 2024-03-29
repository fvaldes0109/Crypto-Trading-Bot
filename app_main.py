import threading
import time
import os

from exchanges.app_kucoin import Kucoin
from exchanges.app_kucoin_virtual import KucoinVirtual
from exchanges.app_kucoin_futures import KucoinFutures
from bots.app_bot import Bot
from app_telegram import telegram_bot
from app_telegram_commands import TelegramCommands

telegram_bot.send('Starting system')

api_key = os.environ['api_key']
api_secret = os.environ['api_secret']
api_passphrase = os.environ['api_passphrase']
is_sandbox = True if os.environ['is_sandbox'] == 'yes' else False

wallet1 = Kucoin('KcWallet', api_key, api_secret, api_passphrase, is_sandbox)
wallet2 = KucoinVirtual('VirtualWallet')
futures = KucoinFutures('KcFutures')
bot1 = Bot('KcBot', wallet1)
bot2 = Bot('VirtualBot', wallet2)
telegram_commands = TelegramCommands(bot1, bot2, wallet1, wallet2, futures)

thread1 = threading.Thread(target=bot1.start_bot)
thread2 = threading.Thread(target=bot2.start_bot)
thread3 = threading.Thread(target=telegram_commands.listen)

thread1.start()
thread2.start()
thread3.start()

thread1.join()
thread2.join()
thread3.join()