import time

from PySide6.QtCore import QThread

from globals import Globals

class Trader(QThread):

    def __init__(self):
        super().__init__()
        self.setObjectName('Trader Thread')

    def run(self):
        #TODO: Implement trading session data live backup and restore;
        while True:
            if Globals.instrumentAllowed and not 'none' in Globals.currentSignal and not Globals.ongoingTrade:
                try:
                    Globals.ongoingTrade, Globals.tradeData = Globals.iqoapi.buy(Globals.entryAmount, Globals.instrument, Globals.currentSignal, Globals.expiration)
                    if not Globals.ongoingTrade:
                        time.sleep(Globals.LOW_PRIORITY_MS)
                        continue

                    Globals.totalMadeEntries += 1
                    Globals.lastSignal = Globals.currentSignal
                    Globals.currentSignal = 'none'

                    tradeResult = Globals.iqoapi.check_win_v4(Globals.tradeData)
                    Globals.ongoingTrade = False
                    Globals.sessionBalanceStatus += tradeResult[1]
                    if tradeResult[0] == 'win':
                        Globals.totalWin += 1
                        if Globals.useMartingale and Globals.martingaleLevel > 0:
                            Globals.martingaleLevel = 0
                            Globals.entryAmount = Globals.minimumEntryAmount
                    elif tradeResult[0] == 'loose':
                        #TODO: Implement a trade signal cooldown to avoid sequencial entries on lateral/bad markets; ⏳
                        #TODO: Implement martingale auto management; ✅
                        Globals.totalLoss += 1
                        if Globals.useMartingale and Globals.martingaleLevel <= Globals.martingaleMax:
                            Globals.martingaleLevel += 1
                            if Globals.martingaleLevel > Globals.martingaleHigh: Globals.martingaleHigh = Globals.martingaleLevel
                            Globals.entryAmount *= 2
                        else:
                            Globals.martingaleLevel = 0
                            Globals.entryAmount = Globals.minimumEntryAmount
                    elif tradeResult[0] == 'equal':
                        Globals.totalDraw += 1
                except:
                    time.sleep(Globals.LOW_PRIORITY_MS)
                    continue
            time.sleep(Globals.HIGH_PRIORITY_MS)

    def martingale():
        pass