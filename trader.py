import time

from PySide6.QtCore import QThread

from globals import Globals

class Trader(QThread):

    def __init__(self):
        super().__init__()
        self.setObjectName("Trader Thread")

    def run(self):
        tradeData = []
        while True:
            if Globals.instrumentAllowed and not 'none' in Globals.currentSignal:
                try:
                    tradeData = Globals.iqoapi.buy_order(Globals.INSTRUMENTS[Globals.PAIR]['TYPE'], Globals.INSTRUMENTS[Globals.PAIR]['ID'],
                                                   Globals.currentSignal, Globals.entryAmount, Globals.INSTRUMENTS[Globals.PAIR]['LEVERAGE'],
                                                   'market', None, None, 'percent', Globals.STOP_LOSS_PERCENT, 'percent',
                                                   Globals.TAKE_PROFIT_PERCENT, Globals.USE_TRAIL_STOP)
                    if not tradeData[0]:
                        time.sleep(Globals.LOW_PRIORITY_MS)
                        continue
                    Globals.ongoingTrades += 1
                    Globals.lastSignal = Globals.currentSignal
                    Globals.currentSignal = 'none'

                    while True:
                        time.sleep(Globals.HIGH_PRIORITY_MS)
                        try:
                            pData = Globals.iqoapi.get_position(tradeData[1])
                            if pData[1]['position']['status'] == 'closed':
                                break
                            else:
                                aData = Globals.iqoapi.get_async_order(tradeData[1])
                                Globals.realTimePnl = aData['position-changed']['msg']['pnl']

                            if Globals.currentSignal != 'none':
                                if Globals.currentSignal is not Globals.lastSignal:
                                    Globals.iqoapi.close_position(tradeData[1])
                        except:
                            continue
                    if float(pData[1]['position']['pnl_realized']) >= 0.00:
                        Globals.totalWin += 1
                    else:
                        Globals.totalLoss += 1
                    Globals.sessionBalanceStatus += float(pData[1]['position']['pnl_realized'])
                    Globals.totalMadeEntries += 1
                    Globals.ongoingTrades -= 1
                except:
                    time.sleep(Globals.LOW_PRIORITY_MS)
                    continue
            time.sleep(Globals.HIGH_PRIORITY_MS)
