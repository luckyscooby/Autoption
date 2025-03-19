import time

from globals import Globals

class Trader():

    def run():
        #TODO: Implement trading session data live backup and restore;
        while True:
            time.sleep(Globals.HIGH_PRIORITY_MS)

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
                    
                    Globals.sessionBalanceStatus += tradeResult[1]

                    if tradeResult[0] == 'win':
                        Globals.totalWin += 1

                        if Globals.USE_STOP_LOSS:
                            Globals.stopLossCooldown = Globals.INITIAL_LOSS_COOLDOWN
                            Globals.stopLossCounter = 0
                            Globals.isOnStopLoss = False

                        if Globals.USE_MARTINGALE and Globals.martingaleLevel > 0:
                            Globals.martingaleLevel = 0
                            Globals.entryAmount = Globals.minimumEntryAmount
                    elif tradeResult[0] == 'loose':
                        Globals.totalLoss += 1

                        if Globals.USE_MARTINGALE and Globals.martingaleLevel <= Globals.MAX_MARTINGALE:
                            Globals.martingaleLevel += 1
                            if Globals.martingaleLevel > Globals.martingaleHigh: Globals.martingaleHigh = Globals.martingaleLevel
                            Globals.entryAmount *= 2
                        else:
                            Globals.martingaleLevel = 0
                            Globals.entryAmount = Globals.minimumEntryAmount

                        if Globals.USE_STOP_LOSS:
                            Globals.isOnStopLoss = True
                            Globals.stopLossCounter = Globals.stopLossCooldown
                            while Globals.stopLossCounter > 0:
                                Globals.stopLossCounter -= 1
                                time.sleep(60)
                            Globals.stopLossCooldown *= Globals.STOP_LOSS_APLIFIER_FACTOR

                    elif tradeResult[0] == 'equal':
                        Globals.totalDraw += 1

                    Globals.ongoingTrade = False
                except:
                    pass
            