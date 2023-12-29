import time

from PySide6.QtCore import QThread

from globals import Globals

class Statistics(QThread):

    def __init__(self):
        super().__init__()
        self.setObjectName("Statistics Thread")

    def run(self):
        try:
            Globals.iqoapi.change_balance(Globals.balanceType)
            Globals.iqoapi.reset_practice_balance()
        except:
            pass

        while True:
            if Globals.totalWin > 0: Globals.assertivityScore = round((Globals.totalWin / (Globals.totalWin + Globals.totalLoss)) * 100, 2)
            if Globals.assertivityScore > Globals.assertHigh: Globals.assertHigh = Globals.assertivityScore
            if Globals.assertLow == 0: Globals.assertLow = Globals.assertivityScore
            if Globals.assertivityScore < Globals.assertLow: Globals.assertLow = Globals.assertivityScore
            if Globals.sessionBalanceStatus > Globals.sessionBalanceHigh: Globals.sessionBalanceHigh = Globals.sessionBalanceStatus
            if Globals.sessionBalanceStatus < Globals.sessionBalanceLow: Globals.sessionBalanceLow = Globals.sessionBalanceStatus
            if Globals.is_connected:
                try:
                    Globals.accountBalance = float(round(Globals.iqoapi.get_balance(), 2))
                except:
                    pass
            time.sleep(Globals.LOW_PRIORITY_MS)
