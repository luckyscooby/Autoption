import os
import time
from datetime import datetime
from termcolor import colored, cprint

from PySide6.QtCore import QThread

from globals import Globals

class UI(QThread):

    def __init__(self):
        super().__init__()
        self.setObjectName("UI Thread")

    def run(self):
        while True:
            os.system(Globals.clsstr)
            print(colored('Autoption', 'blue', None, ['bold']) + colored(' [for IQOption]', 'white', None, ['dark']) + colored(' v' + Globals.VERSION + ' (API v' + Globals.IQOAPI_VERSION + ')', 'grey', None, ['dark']))
            
            elapsed_time = datetime.now() - datetime.fromtimestamp(Globals.unix_start_time)
            elapsed_hours, remainder = divmod(elapsed_time.seconds, 3600)
            elapsed_minutes, elapsed_seconds = divmod(remainder, 60)
            cprint(f'Start @ {Globals.start_time} | Elapsed: {elapsed_time.days}:{elapsed_hours:02d}:{elapsed_minutes:02d}:{elapsed_seconds:02d}')
            
            print(colored('Connected', 'green')) if Globals.is_connected else print(colored('Connection Lost', 'red'))
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
            try:
                if Globals.accountBalance >= Globals.entryAmount:
                    riskFactor = Globals.entryAmount / Globals.accountBalance
                    if riskFactor == 0:
                        riskFactor = 1
                    print('\t' + colored('R$' + "{:.2f}".format(Globals.accountBalance), 'green', None, ['bold']) + ' (' + Globals.balanceType + ') (' + "{:.2f}".format((riskFactor) * 100, 2) + '% Balance Risk)')
            except:
                pass
            print('\tInstrument: ' + colored('EURUSD', 'yellow'), end='')
            if (Globals.lastCandleClose is not None):
                print(' - Last Candle Close: ' + colored("{:.6f}".format(Globals.lastCandleClose), Globals.lastCandleDirection, None, ['bold']), end=' | ')
            if (Globals.wma20 is not None):
                print('WMA(20): ' + colored("{:.5f}".format(Globals.wma20), 'magenta', None, ['bold']), end=' | ')
            if Globals.isBearish or Globals.isBullish:
                if Globals.isBullish:
                    print(colored('▲ Uptrend', 'green', None, ['bold']), end='')
                elif Globals.isBearish:
                    print(colored('▼ Downtrend', 'red', None, ['bold']), end='')
            #if (Globals.predictionPrice is not None):
            #    print(' Prediction: ' + colored("{:.6f}".format(Globals.predictionPrice), 'magenta', None, ['bold']))
            # if(Globals.yhat[0] is not None):
            # print(' (RQKernel ' + colored("{:.6f}".format(Globals.forecastK), 'magenta', None, ['dark']), end='')
            # if(Globals.forecastP is not None):
            # print(' & Prophet ' + colored("{:.6f}".format(Globals.forecastP['yhat'][0]) , 'magenta', None, ['dark']) + ')')
            # fig = Globals.pf.plot(Globals.forecastP)
            # fiGlobals.show()

            if not Globals.is_connected:
                print(colored('\tWaiting Reconnection...', 'red', None, ['dark']))
            else:
                if Globals.instrumentAllowed:
                    #if Globals.ongoingTrade:
                       #print('\tApprox. PnL: ' + colored('R$+' + str(Globals.orderCloseTime), 'green') if Globals.orderCloseTime >= 0 else print(
                            #'\tApprox. PnL: ' + colored('R$' + str(Globals.orderCloseTime), 'red')))
                    #else:
                    print(colored('\tSurfing Market...', 'cyan', None, ['bold']))
                else:
                    print(colored('\tWaiting clearance; Reason: ' + Globals.conditionerReason, 'cyan', None, ['dark']))
            time.sleep(Globals.NORMAL_PRIORITY_MS)
