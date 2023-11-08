import os
import time
from datetime import datetime
from termcolor import colored

from PySide6.QtCore import QRunnable

from globals import Globals

class UI(QRunnable):

    def run(self):
        while True:
            os.system(Globals.clsstr)
            print(colored('Autoption', 'blue', None, ['bold']) + colored(' [for IQOption]', 'white', None, ['dark']) + colored(' v' + Globals.VERSION, 'grey', None, ['dark']))
            print('STime: ' + Globals.start_time + ' | CTime: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print(colored('Connected', 'green')) if Globals.is_connected else print(colored('Disconnected', 'red'))
            print(colored(
                '\tAssertiveness: ' + str(Globals.assertivityScore) + '% (High: ' + str(Globals.assertHigh) + '% / Low: ' + str(
                    Globals.assertLow) + '%)', None, None, ['bold']) + ' @ M' + str(
                Globals.timeframe.denominator)) if Globals.assertivityScore > 0 else print(
                colored('\tAssertiveness: 0%', None, None, ['bold']) + ' @ M' + str(Globals.timeframe.denominator))
            print('\tP: ' + colored(str(Globals.totalWin), 'green') + ' / L: ' + colored(str(Globals.totalLoss),
                                                                                   'red') + ' / T: ' + colored(
                str(Globals.totalMadeEntries), 'white', None, ['dark', 'bold']))
            print('\tConsolidated Profit: ' + colored('R$' + "{:.2f}".format(Globals.sessionBalanceStatus), 'green', None,
                                                      ['bold']) + ' (High: ' + 'R$' + "{:.2f}".format(
                Globals.sessionBalanceHigh) + ' / Low: ' + 'R$' + "{:.2f}".format(
                Globals.sessionBalanceLow) + ')') if Globals.sessionBalanceStatus >= 0 else print(
                '\tConsolidated Damage: ' + colored('R$' + "{:.2f}".format(abs(Globals.sessionBalanceStatus)), 'red', None,
                                                    ['bold']) + ' (High: ' + 'R$' + "{:.2f}".format(
                    Globals.sessionBalanceHigh) + ' / Low: ' + 'R$' + "{:.2f}".format(Globals.sessionBalanceLow) + ')')
            print('\t' + colored('R$' + "{:.2f}".format(Globals.accountBalance), 'green', None,
                                 ['bold']) + ' (' + Globals.balanceType + ') (' + "{:.2f}".format(
                (Globals.entryAmount / Globals.accountBalance) * 100, 2) + '% Balance Risk)')
            print('\tInstrument: ' + colored(Globals.PAIR, 'yellow'), end='')
            if (Globals.lastPrice is not None):
                print(' - Last Price: ' + colored("{:.6f}".format(Globals.lastPrice), 'yellow', None, ['bold']), end='')
            if Globals.isBearish or Globals.isBullish:
                if Globals.isBullish:
                    print(colored(' ▲ Uptrend', 'green', None, ['bold']), end='')
                elif Globals.isBearish:
                    print(colored(' ▼ Downtrend', 'red', None, ['bold']), end='')
            if (Globals.predictionPrice is not None):
                print(' Prediction: ' + colored("{:.6f}".format(Globals.predictionPrice), 'magenta', None, ['bold']))
            # if(Globals.yhat[0] is not None):
            # print(' (RQKernel ' + colored("{:.6f}".format(Globals.forecastK), 'magenta', None, ['dark']), end='')
            # if(Globals.forecastP is not None):
            # print(' & Prophet ' + colored("{:.6f}".format(Globals.forecastP['yhat'][0]) , 'magenta', None, ['dark']) + ')')
            # fig = Globals.pf.plot(Globals.forecastP)
            # fiGlobals.show()

            if not Globals.is_connected:
                print(colored('\tWaiting Connection...', 'red', None, ['dark']))
            else:
                if Globals.instrumentAllowed:
                    if Globals.ongoingTrades > 0:
                        print('\tApprox. PnL: ' + colored('+R$' + str(Globals.realTimePnl)),
                              'green') if Globals.realTimePnl >= 0.00 else print(
                            '\tApprox. PnL: ' + colored('-R$' + str(abs(round(Globals.realTimePnl, 2))), 'red'))
                    else:
                        print(colored('\tSurfing Market...', 'cyan', None, ['bold']))
                else:
                    print(colored('\tWaiting Clearance...', 'cyan', None, ['dark']))
            time.sleep(Globals.NORMAL_PRIORITY_MS)
