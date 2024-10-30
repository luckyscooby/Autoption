import time

from globals import Globals

class Statistics():

    def run():
        while True:
            time.sleep(Globals.LOW_PRIORITY_MS)

            if Globals.totalWin > 0 and Globals.totalLoss > 0: Globals.assertivityScore = round((Globals.totalWin / (Globals.totalWin + Globals.totalLoss)) * 100, 2)
            if Globals.assertivityScore > Globals.assertHigh: Globals.assertHigh = Globals.assertivityScore
            if Globals.assertLow == 0: Globals.assertLow = Globals.assertivityScore
            if Globals.assertivityScore < Globals.assertLow: Globals.assertLow = Globals.assertivityScore

            if Globals.sessionBalanceStatus > Globals.sessionBalanceHigh: Globals.sessionBalanceHigh = Globals.sessionBalanceStatus
            if Globals.sessionBalanceStatus < Globals.sessionBalanceLow: Globals.sessionBalanceLow = Globals.sessionBalanceStatus

            if Globals.is_connected: Statistics.getBalance()
            #if Globals.ongoingTrade: Globals.orderCloseTime = round(Globals.iqoapi.get_async_order(Globals.tradeData)['position-changed']['msg']['pnl'], 2)   

    @staticmethod
    def getBalance():
        try:
            Globals.accountBalance = float(round(Globals.iqoapi.get_balance(), 2))
        except:
            pass