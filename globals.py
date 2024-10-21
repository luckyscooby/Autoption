import os

from enum import Enum
from pyqoptionapi.stable_api import IQ_Option

class Globals:

    VERSION = '0.50 (Alpha 5)'
    IQOAPI_VERSION = IQ_Option.__version__

    class Timeframe(Enum):
        M1 = 60

    iqoapi = IQ_Option(email=os.getenv(key='email'), password=os.getenv('password')) # Manually create a file '.env' containg two lines: email=youremail@email.com & password=yourPassword  
    clsstr = ''
    unix_start_time = None
    start_time = None
    is_connected = False
    balanceType = 'PRACTICE' # 'PRACTICE' or 'REAL'
    instrument = 'EURUSD'
    timeframe = Timeframe.M1.value
    expiration = 5 # Minutes
    useLossCooldown = False
    useMartingale = True
    martingaleLevel = 0
    martingaleMax = 5
    martingaleHigh = 0
    currency = ''
    accountBalance = 0.00
    sessionBalanceStatus = 0.00
    sessionBalanceHigh = 0.00
    sessionBalanceLow = 0.00
    minimumEntryAmount = 0.00
    entryAmount = 0.00 # TODO: Implement it to programaticaly retrieve the minimum entry amount according to balanceType; ✅
    assertivityScore = 0.0
    assertHigh = 0.0
    assertLow = 0.0
    totalLoss = 0
    totalDraw = 0
    totalWin = 0
    totalMadeEntries = 0
    tradeData = None
    #orderCloseTime = None
    conditionerReason = 'initializing'
 
    # WMA(20)
    wma20 = None

    lastCandleDirection = None
    lastCandleClose = None
    isBearish = False
    isBullish = False
    isBearishChange = False
    isBullishChange = False

    # THREAD SEMAPHORES
    currentSignal = 'none'
    lastSignal = 'none'
    instrumentAllowed = False
    ongoingTrade = False

    # THREAD SLEEP PRIORITIES
    # These values are in seconds for use in time.sleep() during loops/cycles;
    HIGH_PRIORITY_MS = 0.34
    NORMAL_PRIORITY_MS = 0.67
    LOW_PRIORITY_MS = 1.00
