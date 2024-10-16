import time

from PySide6.QtCore import QThread

from globals import Globals

class Trader(QThread):

    def __init__(self):
        super().__init__()
        self.setObjectName("Trader Thread")

    def run(self):
        while True:
            if Globals.instrumentAllowed and not 'none' in Globals.currentSignal and not Globals.ongoingTrade:
                try:
                    Globals.ongoingTrade, Globals.tradeData = Globals.iqoapi.buy(Globals.entryAmount, "EURUSD", Globals.currentSignal, 5)
                    if not Globals.ongoingTrade:
                        time.sleep(Globals.LOW_PRIORITY_MS)
                        continue

                    Globals.lastSignal = Globals.currentSignal
                    Globals.currentSignal = 'none'

                    tradeResult = Globals.iqoapi.check_win_v4(Globals.tradeData)

                    if tradeResult[0] == "win":
                        Globals.totalWin += 1
                    elif tradeResult[0] == "loose":
                        #TODO: Implement a trade signal cooldown to avoid sequencial entries on lateral/bad markets;
                        Globals.totalLoss += 1
                    elif tradeResult[0] == "equal":
                        Globals.totalDraw += 1

                    Globals.totalMadeEntries += 1
                    Globals.ongoingTrade = False

                    Globals.sessionBalanceStatus += tradeResult[1]
                    
                except:
                    time.sleep(Globals.LOW_PRIORITY_MS)
                    continue
            time.sleep(Globals.HIGH_PRIORITY_MS)

    def martingale():
        pass