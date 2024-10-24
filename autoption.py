
#TODO: Implement persistent logging for later strategy performance analysis;

import os
import time
import threading
import logging

from datetime import datetime
from termcolor import cprint

from globals import Globals
from ui import UI
from connector import Connection
from conditioner import Conditioner
from analyser import Analyser
from trader import Trader
from stats import Statistics

threading.current_thread().setName('Autoption MainThread')
logging.getLogger().setLevel(level=logging.DEBUG)
#logging.setLevel(logging.INFO)
#logging.disable(level=logging.CRITICAL)

if os.name == 'posix':
    Globals.clsstr = 'clear'
elif os.name == 'nt':
    Globals.clsstr = 'cls'

# SETUP IQOPTION ENVIRONMENT
Connection.connect()
Globals.iqoapi.reset_practice_balance()
Globals.iqoapi.change_balance(Globals.balanceType)
Globals.currency = Globals.iqoapi.get_currency()
Globals.minimumEntryAmount = Globals.iqoapi.get_binary_option_detail()['EURUSD']['turbo']['minimal_bet']
Globals.entryAmount = Globals.minimumEntryAmount

Globals.unix_start_time = time.time()
Globals.start_time = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p') + ' (' + time.localtime().tm_zone + ')'

###

###

# LAUNCH MAIN THREADS
try:
    uiThread = threading.Thread(target=Connection.run, name='Connection Thread')
    connectionThread = threading.Thread(target=UI.run, name='UI Thread')
    conditionerThread = threading.Thread(target=Conditioner.run, name='Conditioner Thread')
    analyserThread = threading.Thread(target=Analyser.run, name='Analyser Thread')
    traderThread = threading.Thread(target=Trader.run, name='Trader Thread')
    statisticsThread = threading.Thread(target=Statistics.run, name='Statistics Thread')

    uiThread.start()
    connectionThread.start()
    conditionerThread.start()
    analyserThread.start()
    traderThread.start()
    statisticsThread.start()

    # MainThread MUST be kept alive for iqoptionapi to work properly
    threading.current_thread().priority = 1
    #uiThread.wait(deadline=QDeadlineTimer(QDeadlineTimer.Forever))
    #uiThread.join()

except:
    cprint('Thread Error, Abort', 'red')
    exit()