from iqoptionapi.stable_api import IQ_Option
from enum import Enum
from collections import defaultdict
from prophet import Prophet

VERSION = '0.29.2'


class Timeframe(Enum):
	M1 = 60
	M2 = 120
	M5 = 300
	M10 = 600
	M15 = 900
	M30 = 1800
	
	H1 = 3600
	H2 = 7200
	H4 = 14400
	H8 = 28800
	H12 = 43200
	
	D1 = 86400


INSTRUMENTS = defaultdict(lambda: defaultdict(dict))
#
INSTRUMENTS['EURUSD-50']['TYPE'] = 'forex'
INSTRUMENTS['EURUSD-50']['ID'] = 'EURUSD'
INSTRUMENTS['EURUSD-50']['LEVERAGE'] = 50
INSTRUMENTS['EURUSD-50']['MAX_SPREAD'] = 0.005
INSTRUMENTS['EURUSD-50']['SESSION'] = [12, 16]
#
INSTRUMENTS['EURUSD-100']['TYPE'] = 'forex'
INSTRUMENTS['EURUSD-100']['ID'] = 'EURUSD'
INSTRUMENTS['EURUSD-100']['LEVERAGE'] = 100
INSTRUMENTS['EURUSD-100']['MAX_SPREAD'] = 0.005
INSTRUMENTS['EURUSD-100']['SESSION'] = [12, 16]
#
INSTRUMENTS['EURUSD-200']['TYPE'] = 'forex'
INSTRUMENTS['EURUSD-200']['ID'] = 'EURUSD'
INSTRUMENTS['EURUSD-200']['LEVERAGE'] = 200
INSTRUMENTS['EURUSD-200']['MAX_SPREAD'] = 0.005
INSTRUMENTS['EURUSD-200']['SESSION'] = [12, 16]
#
INSTRUMENTS['EURUSD-300']['TYPE'] = 'forex'
INSTRUMENTS['EURUSD-300']['ID'] = 'EURUSD'
INSTRUMENTS['EURUSD-300']['LEVERAGE'] = 500
INSTRUMENTS['EURUSD-300']['MAX_SPREAD'] = 0.005
INSTRUMENTS['EURUSD-300']['SESSION'] = [12, 16]
#
INSTRUMENTS['EURUSD-500']['TYPE'] = 'forex'
INSTRUMENTS['EURUSD-500']['ID'] = 'EURUSD'
INSTRUMENTS['EURUSD-500']['LEVERAGE'] = 500
INSTRUMENTS['EURUSD-500']['MAX_SPREAD'] = 0.005
INSTRUMENTS['EURUSD-500']['SESSION'] = [12, 16]
#
INSTRUMENTS['EURUSD-1000']['TYPE'] = 'forex'
INSTRUMENTS['EURUSD-1000']['ID'] = 'EURUSD'
INSTRUMENTS['EURUSD-1000']['LEVERAGE'] = 1000
INSTRUMENTS['EURUSD-1000']['MAX_SPREAD'] = 0.005
INSTRUMENTS['EURUSD-1000']['SESSION'] = [12, 16]
#
INSTRUMENTS['BTCUSD-100']['TYPE'] = 'crypto'
INSTRUMENTS['BTCUSD-100']['ID'] = 'BTCUSD-L'
INSTRUMENTS['BTCUSD-100']['LEVERAGE'] = 100
INSTRUMENTS['BTCUSD-100']['MAX_SPREAD'] = 25
INSTRUMENTS['BTCUSD-100']['SESSION'] = [00, 24]
#
INSTRUMENTS['BTCUSD-5']['TYPE'] = 'crypto'
INSTRUMENTS['BTCUSD-5']['ID'] = 'BTCUSD'
INSTRUMENTS['BTCUSD-5']['LEVERAGE'] = 5
INSTRUMENTS['BTCUSD-5']['MAX_SPREAD'] = 95
INSTRUMENTS['BTCUSD-5']['SESSION'] = [00, 24]

iqoapi = IQ_Option('your@email.com', 'YourPassword')
start_time = None
is_connected = False
balanceType = 'Practice'
accountBalance = 0
sessionBalanceStatus = 0.00
sessionBalanceHigh = 0.00
sessionBalanceLow = 0.00
entryAmount = 2.00
PAIR = 'BTCUSD-100'
STOP_LOSS_PERCENT = 20     #%
TAKE_PROFIT_PERCENT = 50	#%
USE_TRAIL_STOP = True
assertivityScore = 0.00
assertHigh = 0.00
assertLow = 0.00
totalLoss = 0
totalWin = 0
totalMadeEntries = 0
ongoingTrades = 0
realTimePnl = 0.00
timeframe = Timeframe.M1.value
isBearish = False
isBullish = False
isBearishChange = False
isBullishChange = False
clsstr = ''


# Prophet
yhat = [None, None]
price = [None, None]
pf = Prophet()
forecast = None
predictionPrice = None
lastPrice = None

# THREAD SEMAPHORES
currentSignal = 'none'
lastSignal = 'none'
instrumentAllowed = False

# THREAD SLEEP PRIORITIES
HIGH_PRIORITY_MS = 0.33
NORMAL_PRIORITY_MS = 0.66
LOW_PRIORITY_MS = 0.99
