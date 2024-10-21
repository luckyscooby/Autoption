import os
import time

from datetime import datetime
from termcolor import colored, cprint

from globals import Globals

class UI():

    def run():
        while True:
            os.system(Globals.clsstr)
            print(colored('Autoption', 'blue', None, ['bold', 'underline']) + colored(' [for IQOption]', 'white', None, ['dark']) + colored(' v' + Globals.VERSION + ' [API v' + Globals.IQOAPI_VERSION + ']', 'grey', None, ['dark']))
            
            elapsed_time = datetime.now() - datetime.fromtimestamp(Globals.unix_start_time)
            elapsed_hours, remainder = divmod(elapsed_time.seconds, 3600)
            elapsed_minutes, elapsed_seconds = divmod(remainder, 60)
            cprint(f'Start @ {Globals.start_time} | Elapsed: {elapsed_time.days}:{elapsed_hours:02d}:{elapsed_minutes:02d}:{elapsed_seconds:02d}')
            
            print(colored('Connected', 'green')) if Globals.is_connected else print(colored('Connection Lost', 'red'))
            print(colored(
                '\tAssertiveness: ' + str(Globals.assertivityScore) + '% (High: ' + str(Globals.assertHigh) + '% / Low: ' + str(
                    Globals.assertLow) + '%)', color='white', attrs=['bold']) + ' @ M' + str(
                Globals.timeframe.denominator) + ':' + str(Globals.expiration)) if Globals.assertivityScore > 0 else print(
                colored('\tUnknown Assertiveness', color='white', attrs=['bold']) + ' @ M' + str(Globals.timeframe.denominator) + ':' + str(Globals.expiration))
            print('\tWin: ' + colored(str(Globals.totalWin), 'light_green') + ' / Loss: ' + colored(str(Globals.totalLoss),
                                                                                   'red') + ' / Draw: ' + colored(str(Globals.totalDraw),
                                                                                   'grey') + ' / Total Entries: ' + colored(
                str(Globals.totalMadeEntries), 'white', None, ['dark', 'bold']))
            print('\tMartingale Level: ' + Globals.martingaleLevel.__str__() + ' (Max: ' + Globals.martingaleMax.__str__() + ') / High: ' + Globals.martingaleHigh.__str__())
            try:
                if Globals.accountBalance >= Globals.entryAmount:
                    riskFactor = Globals.entryAmount / Globals.accountBalance
                    if riskFactor == 0:
                        riskFactor = 1
                    print('\tBalance: ' + colored('$' + '{:.2f}'.format(Globals.accountBalance), 'yellow', attrs=['bold']) + ' (' + colored(Globals.balanceType, color='white', attrs=['bold']) + ') (' + colored(Globals.currency, color='yellow', attrs=['dark']) + ') (' + '{:.2f}'.format((riskFactor) * 100, 2) + '% Balance Risk) ('
                          + colored('Entry Amount: $' + '{:.2f}'.format(Globals.entryAmount), color='yellow', attrs=['dark']) + ')')
            except:
                pass
            print('\tConsolidated Profit: ' + colored('$' + '{:.2f}'.format(Globals.sessionBalanceStatus), 'green', None,
                                                      ['bold']) + ' (High: ' + '$' + '{:.2f}'.format(
                Globals.sessionBalanceHigh) + ' / Low: ' + '$' + '{:.2f}'.format(
                Globals.sessionBalanceLow) + ')') if Globals.sessionBalanceStatus >= 0 else print(
                '\tConsolidated Damage: ' + colored('$' + '{:.2f}'.format(abs(Globals.sessionBalanceStatus)), 'red', None,
                                                    ['bold']) + ' (High: ' + '$' + '{:.2f}'.format(
                    Globals.sessionBalanceHigh) + ' / Low: ' + '$' + '{:.2f}'.format(Globals.sessionBalanceLow) + ')')
            print('\tInstrument: ' + colored(Globals.instrument, 'yellow', attrs=['bold', 'dark']))
            if (Globals.lastCandleClose is not None):
                print('\tLast Candle Close: ' + colored('{:.6f}'.format(Globals.lastCandleClose), Globals.lastCandleDirection, None, ['bold']), end=' | ')
            if (Globals.wma20 is not None):
                print('WMA(20): ' + colored('{:.5f}'.format(Globals.wma20), 'magenta', None, ['bold']), end=' | ')
            if Globals.isBearish or Globals.isBullish:
                if Globals.isBullish:
                    print(colored('▲ Uptrend', 'green', None, ['bold']))
                elif Globals.isBearish:
                    print(colored('▼ Downtrend', 'red', None, ['bold']))

            if not Globals.is_connected:
                cprint('\tWaiting Reconnection...', 'red', None, ['dark', 'bold', 'blink'])
            else:
                if Globals.instrumentAllowed:
                    if Globals.ongoingTrade:
                        #TODO: Show details of trading data as remaining time, PnL and realtime status (win / loss / draw);
                       #print('\tApprox. PnL: ' + colored('$+' + str(Globals.orderCloseTime), 'green') if Globals.orderCloseTime >= 0 else print(
                            #'\tApprox. PnL: ' + colored('$' + str(Globals.orderCloseTime), 'red')))
                        cprint('\tTrading!', 'light_yellow', attrs=['blink', 'bold'])
                    else:
                        cprint('\tSurfing Market...', 'cyan', attrs=['bold', 'blink'])
                else:
                    print(colored('\tWaiting clearance; reason: ', color='red', attrs=['dark']) + colored(Globals.conditionerReason, 'red', attrs=['dark', 'bold', 'blink']))
            time.sleep(Globals.NORMAL_PRIORITY_MS)
