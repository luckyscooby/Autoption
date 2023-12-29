from enum import Enum
from pyqoptionapi.stable_api import IQ_Option
from prophet import Prophet

class Globals:

    VERSION = '0.31.1 Alpha'

    class Timeframe(Enum):
        M1 = 60
        M5 = 300

    iqoapi = IQ_Option('your@email.com', 'yourPassword')
    clsstr = ''
    unix_start_time = None
    start_time = None
    is_connected = False
    balanceType = 'PRACTICE' # 'PRACTICE' or 'REAL'
    accountBalance = 0
    sessionBalanceStatus = 0.00
    sessionBalanceHigh = 0.00
    sessionBalanceLow = 0.00
    entryAmount = 2.00 # TODO: Implement it to programaticaly retrieve the minimum entry amount according to balanceType;
    assertivityScore = 0.00
    assertHigh = 0.00
    assertLow = 0.00
    totalLoss = 0
    totalDraw = 0
    totalWin = 0
    totalMadeEntries = 0
    ongoingTrades = 0
    realTimePnl = 0.00
    timeframe = Timeframe.M1.value

    # WMA(20)
    wma20 = None

    # Prophet
    yhat = [None, None]
    price = [None, None]
    pf = Prophet()
    forecast = None
    predictionPrice = None
    lastCandleClose = None
    lastCandleDirection = None

    isBearish = False
    isBullish = False
    isBearishChange = False
    isBullishChange = False

    # THREAD SEMAPHORES
    currentSignal = 'none'
    lastSignal = 'none'
    instrumentAllowed = False

    # THREAD SLEEP PRIORITIES
    # These values are in seconds for use in time.sleep() during loops/cycles;
    HIGH_PRIORITY_MS = 0.33
    NORMAL_PRIORITY_MS = 0.66
    LOW_PRIORITY_MS = 0.99
