from collections import defaultdict
from enum import Enum

from iqoptionapi.stable_api import IQ_Option
from prophet import Prophet

class Globals:

    VERSION = '0.30.0 Alpha'

    class Timeframe(Enum):
        M1 = 60
        M2 = 120
        M5 = 300
        M10 = 600
        M15 = 900

    INSTRUMENTS = defaultdict(lambda: defaultdict(dict))
    #
    INSTRUMENTS['EURUSD']['TYPE'] = 'turbo'
    INSTRUMENTS['EURUSD']['ID'] = 'EURUSD'
    INSTRUMENTS['EURUSD']['SESSION'] = [9, 14]

    iqoapi = IQ_Option('dummy@mail.com', 'dummyPassword')
    start_time = None
    is_connected = False
    balanceType = 'Practice'
    accountBalance = 0
    sessionBalanceStatus = 0.00
    sessionBalanceHigh = 0.00
    sessionBalanceLow = 0.00
    entryAmount = 2.00
    PAIR = 'EURUSD'
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
    availableAssets = None

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
