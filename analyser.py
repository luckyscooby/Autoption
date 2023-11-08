import os
import time
from datetime import datetime
import pandas as pd
import websocket

from prophet import Prophet

from PySide6.QtCore import QRunnable

from globals import Globals

analyser_name = 'Profecy'
analyser_version = 'REV5 (22/JAN/2023)'
analyser_coder = 'Michael Leocádio'

loopback = 5

class Analyser(QRunnable):

    def run(self):
        # Retrieve starting from oldest candle and excluding latest (not done) one.

        while True:
            if Globals.instrumentAllowed:
                microTime = int(datetime.now().strftime('%S'))
                if microTime == 0:
                    try:
                        instrumentCandles = Globals.iqoapi.get_candles(Globals.INSTRUMENTS[Globals.PAIR]['ID'], Globals.timeframe, loopback + 1,
                                                                 time.time())
                        Globals.lastPrice = instrumentCandles[loopback - 1]['close']

                        # Begin of analysis
                        ###################
                        src = {'ds': [], 'y': []}
                        i = 0
                        while i < (loopback - 1):
                            src['ds'].append(pd.to_datetime(instrumentCandles[i]['to'], unit='s'))
                            src['y'].append(instrumentCandles[i]['close'])
                            i += 1

                        # Prophet
                        df = pd.DataFrame(src)
                        if Globals.yhat is not None:
                            Globals.pf = Prophet()
                        Globals.pf.fit(df)
                        future = Globals.pf.make_future_dataframe(periods=1)
                        Globals.forecast = Globals.pf.predict(future)
                        Globals.predictionPrice = Globals.forecast['yhat'][0]

                        # Assimilation
                        if Globals.price[0] == None:
                            Globals.price[0] = Globals.lastPrice
                            Globals.price[1] = Globals.price[0]
                            Globals.yhat[0] = Globals.predictionPrice
                            Globals.yhat[1] = Globals.yhat[0]
                        else:
                            Globals.price[1] = Globals.price[0]
                            Globals.price[0] = Globals.lastPrice
                            Globals.yhat[1] = Globals.yhat[0]
                            Globals.yhat[0] = Globals.predictionPrice

                            # Crossover Logic
                            Globals.isBearishChange = Globals.price[1] > Globals.yhat[1] and Globals.price[0] < Globals.yhat[0]
                            Globals.isBullishChange = Globals.price[1] < Globals.yhat[1] and Globals.price[0] > Globals.yhat[0]

                        # Trend
                        Globals.isBearish = Globals.yhat[0] > Globals.price[0]
                        Globals.isBullish = Globals.yhat[0] < Globals.price[0]

                        # Signals
                        if Globals.isBullishChange:
                            Globals.currentSignal = 'buy'
                            b = 500
                            while b <= 5000:
                                if os.name == 'posix':
                                    os.system('beep -f ' + str(b) + ' -l 50')
                                b += 500
                        if Globals.isBearishChange:
                            Globals.currentSignal = 'sell'
                            b = 5000
                            while b >= 500:
                                if os.name == 'posix':
                                    os.system('beep -f ' + str(b) + ' -l 50')
                                b -= 500

                        #################
                        # End of analysis

                        time.sleep(Globals.timeframe - 30)
                        continue  # In order to be timeframe agnostic we must cycle each analysis according to given seconds per bar.

                    except (IndexError, TypeError, websocket.WebSocketException) as e:
                        Globals.isConnected = False
            # except:
            #	pass

            time.sleep(Globals.HIGH_PRIORITY_MS)
