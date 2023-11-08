import os
import time
from datetime import datetime
from termcolor import colored

from PySide6.QtCore import QThreadPool

from globals import Globals
from ui import UI
from connector import Connection
from conditioner import Conditioner
from analyser import Analyser
from trader import Trader
from stats import Statistics

if os.name == 'posix':
    Globals.clsstr = 'clear'
elif os.name == 'nt':
    Globals.clsstr = 'cls'

Connection.connect()
Globals.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# SET BALANCE
Globals.iqoapi.change_balance(Globals.balanceType.upper())
#g.iqoapi.reset_practice_balance()
Globals.accountBalance = Statistics._M_AccountBalance()

#availableAssets = g.iqoapi.get_all_open_time()
#availableAssets = g.iqoapi.__get_binary_open()

# LAUNCH MAIN THREADS
try:
    qThreadPool = QThreadPool()

    uiThread = UI()
    connectionThread = Connection()
    conditionerThread = Conditioner()
    analyserThread = Analyser()
    traderThread = Trader()
    statisticsThread = Statistics()

    qThreadPool.start(uiThread)
    qThreadPool.start(connectionThread)
    qThreadPool.start(conditionerThread)
    qThreadPool.start(analyserThread)
    qThreadPool.start(traderThread)
    qThreadPool.start(statisticsThread)
except:
    print(colored('Thread Error, Abort', 'red'))
    exit()

# MainThread MUST be kept alive for iqoptionapi to work properly
while True:
    time.sleep(Globals.LOW_PRIORITY_MS)