import time

from PySide6.QtCore import QRunnable

from globals import Globals

class Statistics(QRunnable):

    def run(self):
        while True:
            if Globals.totalWin > 0: Globals.assertivityScore = round((Globals.totalWin / (Globals.totalWin + Globals.totalLoss)) * 100, 2)
            if Globals.assertivityScore > Globals.assertHigh: Globals.assertHigh = Globals.assertivityScore
            if Globals.assertLow == 0: Globals.assertLow = Globals.assertivityScore
            if Globals.assertivityScore < Globals.assertLow: Globals.assertLow = Globals.assertivityScore
            if Globals.sessionBalanceStatus > Globals.sessionBalanceHigh: Globals.sessionBalanceHigh = Globals.sessionBalanceStatus
            if Globals.sessionBalanceStatus < Globals.sessionBalanceLow: Globals.sessionBalanceLow = Globals.sessionBalanceStatus
            Globals.accountBalance = self._M_AccountBalance()
            time.sleep(Globals.LOW_PRIORITY_MS)

    @staticmethod
    def _M_AccountBalance():
        simulatedAmount = 100
        isSimulated = True
        try:
            b = round(Globals.iqoapi.get_balance(), 2)
            if isSimulated:
                return float(b - (10000 - simulatedAmount))
            else:
                return float(round(Globals.iqoapi.get_balance(), 2))
        except:
            return 1
