''' This module is where our technical analysis goes in. It kicks in when a new candle is generated,
retrieves previous candles and performs some calculations to find the WMA(20) [20 periods Weighted Moving Average].
After some experiments and tests, I found out the WMA(20) has a VERY close result that of
Nadaraya-Watson: Rational Quadratic Kernel from jdehorty [https://www.tradingview.com/script/AWNvbPRM-Nadaraya-Watson-Rational-Quadratic-Kernel-Non-Repainting/]
which worked great in my analysis strategy. Both practically 'walk' together on the chart.

The basic idea here is to check for crossovers and emit a buy/sell signal for the trader module.
Of course I will be improving this algorithm in the future, for lateral market checks, for instance.

I'm also experimenting (but not operating with) the Prophet machine learning module, from Meta, for price predictions.
So there will be some output from it for me to analyse.

In summary, this module:
> Waits for instrument to be cleared for trading and for a new candle to comes in (second 0);
> Retrieves the last 20 candles and use it for WMA(20) calculation;
> Checks for a crossover and emits a buy/sell signal to the trader module;

> After this time critical part, it experiments with Prophet using the same retrieved candles data,
but no signal is generated from this (yet).
'''

import time

from datetime import datetime

from globals import Globals

class Analyser():

    def run():
        while True:
            if Globals.instrumentAllowed:
                microTime = int(datetime.now().strftime('%S'))
                if microTime == 0:
                    try:
                        period = 20
                        instrumentCandles = Globals.iqoapi.get_candles(Globals.instrument, Globals.timeframe, period + 1, time.time())
                        if instrumentCandles[period]['close'] > instrumentCandles[period]['open']:
                            Globals.lastCandleDirection = 'green'
                        elif instrumentCandles[period]['close'] < instrumentCandles[period]['open']:
                            Globals.lastCandleDirection = 'red'
                        else:
                            Globals.lastCandleDirection = 'grey'
                        Globals.lastCandleClose = instrumentCandles[period]['close']

                        # Calculate WMA(20)
                        # Formula based on IQOption's own MathML: https://quadcode-tech.github.io/quadcodescript-docs/api/averages/wma.html
                        series = []
                        i = 0
                        while i < (period):
                            series.append(instrumentCandles[i]['close'])
                            i += 1
                        wma_sum_numerator = 0
                        wma_sum_denominator = 0
                        for i in range(0, period - 1):
                            wma_sum_numerator += (period - 1 - i) * series[period - 1 - i]
                            wma_sum_denominator += (period - 1 - i)
                        Globals.wma20 = wma_sum_numerator / wma_sum_denominator

                        # Trend & Crossover Signal
                        #TODO: Implement signal confirmation using the next candle to avoid false crossovers;
                        if not Globals.ongoingTrade:
                            if Globals.wma20 > Globals.lastCandleClose:
                                if (Globals.isBearish or Globals.isBullish) is not False:
                                        if Globals.isBullish:
                                            Globals.currentSignal = 'put' # Crossover = put // Hit = call
                            elif Globals.wma20 < Globals.lastCandleClose:
                                if (Globals.isBearish or Globals.isBullish) is not False:
                                        if Globals.isBearish:
                                            Globals.currentSignal = 'call' # Crossover = call // Hit = put
                        
                        Globals.isBearish = Globals.wma20 > Globals.lastCandleClose
                        Globals.isBullish = Globals.wma20 < Globals.lastCandleClose
                        
                        continue

                        time.sleep(Globals.timeframe - 30)
                        continue  # In order to be timeframe agnostic we must cycle each analysis according to given seconds per bar.

                    except:
                        pass

            time.sleep(Globals.HIGH_PRIORITY_MS)
