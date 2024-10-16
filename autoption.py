import os
import time
import threading
import logging

from datetime import datetime
from termcolor import cprint

from PySide6.QtCore import QThread, QDeadlineTimer

from globals import Globals
from ui import UI
from connector import Connection
from conditioner import Conditioner
from analyser import Analyser
from trader import Trader
from stats import Statistics

import pandas as pd
import numpy as np

threading.current_thread().setName("Autoption MainThread")

#logging.getLogger().setLevel(level=logging.DEBUG)
#logging.setLevel(logging.INFO)
logging.disable(level=logging.CRITICAL)

if os.name == 'posix':
    Globals.clsstr = 'clear'
elif os.name == 'nt':
    Globals.clsstr = 'cls'

Connection.connect()
Globals.unix_start_time = time.time()
Globals.start_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p") + ' (' + time.localtime().tm_zone + ')'

###
#Globals.ongoingTrade, Globals.tradeData = Globals.iqoapi.buy(Globals.entryAmount, "EURUSD", "put", 1)
###

# LAUNCH MAIN THREADS
try:
    uiThread = UI()
    connectionThread = Connection()
    conditionerThread = Conditioner()
    analyserThread = Analyser()
    traderThread = Trader()
    statisticsThread = Statistics()

    uiThread.start()
    connectionThread.start()
    conditionerThread.start(priority=QThread.Priority.TimeCriticalPriority)
    analyserThread.start(priority=QThread.Priority.TimeCriticalPriority)
    traderThread.start(priority=QThread.Priority.TimeCriticalPriority)
    statisticsThread.start(priority=QThread.Priority.LowestPriority)

    # MainThread MUST be kept alive for iqoptionapi to work properly
    threading.current_thread().priority = 1
    uiThread.wait(deadline=QDeadlineTimer(QDeadlineTimer.Forever))

except:
    cprint('Thread Error, Abort', 'red')
    exit()