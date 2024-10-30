''' Thread responsible for telling the analyser and trader modules if the instrument [EURUSD]
is in proper condition for market operation, taking into consideration the following factors:

> IQOption connection (obviously);
> London and New York sessions are overlapping (high trading volumes / volatility during this period for EURUSD);
> Instrument is openned / not suspended in the broker;
> Current profit is equal to or higher than 84% for each win;

I must mention that the code waits for second 30 to perform the three former checks; after some testing I
found this to be the optimal moment each minute (M1 candle). I considered the time it takes for the pyqoptionapi
to retrieve the data and the broker's purchase time:
- when the remaining purchase time reaches 0:30, the clock hits the next minute and a new candle is generated; 
- when the clock hits second 30, the remaining purchase time is reset to 1 minute;
It also helps to reduce unnecessary multiple calls to the server within the same minute, preserving CPU and network resources.

If the instrument is clear to go,
the analyser will know and wait for the very first second of the next candle to perform its job.

(Read analyser.py)
'''

import time

from datetime import datetime, timezone

from globals import Globals

class Conditioner():

    def run():
        while True:
            time.sleep(Globals.HIGH_PRIORITY_MS)

            if not Globals.is_connected:
                Globals.instrumentAllowed = False
                Globals.conditionerReason = 'not connected'
                continue

            if Globals.accountBalance < Globals.minimumEntryAmount:
                Globals.instrumentAllowed = False
                Globals.conditionerReason = 'out of balance'
                continue

            microTime = int(datetime.now().strftime('%S'))
            if microTime == 30:
                # Check if instrument is in proper time for trading, based on London (GMT 0) timezone;
                # Proper time: more volume = more volatility, AVOID lateral markets!
                # For EURUSD this is where the London session (EUR) and the New York session (USD) overlap, between 12pm and 4pm.
                # Reference: https://www.babypips.com/tools/forex-market-hours
                sessionTime = int(datetime.now(tz=timezone.utc).strftime('%H'))
                if not (sessionTime >= 12) and (sessionTime < 17):
                    Globals.instrumentAllowed = False
                    Globals.conditionerReason = 'out of session'
                    continue

                try:
                    # Check if instrument is opened for trading
                    availableAssets = Globals.iqoapi.get_binary_option_detail()
                    if not availableAssets[Globals.instrument]['turbo']['enabled'] or availableAssets[Globals.instrument]['turbo']['is_suspended']:
                        Globals.instrumentAllowed = False
                        Globals.conditionerReason = 'instrument unavailable'
                        continue
                    
                    # Check the current profit percentage; I do not trade with profits below 84% since it affects martingale levels.
                    availableProfit = Globals.iqoapi.get_all_profit()
                    if not availableProfit[Globals.instrument]['turbo'] >= 0.84:
                        Globals.instrumentAllowed = False
                        Globals.conditionerReason = 'profit not optimal (' + str(availableProfit[Globals.instrument]['turbo'] * 100) + '%)'
                        continue

                    Globals.instrumentAllowed = True

                except:
                    Globals.instrumentAllowed = False
                    Globals.conditionerReason = 'unknown expection'
