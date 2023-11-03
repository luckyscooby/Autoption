from datetime import datetime
import websocket
import globals as g
import pandas as pd
from prophet import Prophet
import os
import time

analyser_name = 'Profecy'
analyser_version = 'REV5 (22/JAN/2023)'
analyser_coder = 'Michael Leocádio'	

loopback = 5

def analyse():
	# Retrieve starting from oldest candle and excluding latest (not done) one.

	while True:
		if g.instrumentAllowed:
			microTime = int(datetime.now().strftime('%S'))
			if microTime == 0:
				try:
					instrumentCandles = g.iqoapi.get_candles(g.INSTRUMENTS[g.PAIR]['ID'], g.timeframe, loopback + 1, time.time())
					g.lastPrice = instrumentCandles[loopback - 1]['close']
					
					# Begin of analysis
					###################
					src = {'ds':[], 'y':[]}
					i = 0
					while i < (loopback - 1):
						src['ds'].append(pd.to_datetime(instrumentCandles[i]['to'], unit='s'))
						src['y'].append(instrumentCandles[i]['close'])
						i += 1

					# Prophet
					df = pd.DataFrame(src)
					if g.yhat is not None:
						g.pf = Prophet()
					g.pf.fit(df)
					future = g.pf.make_future_dataframe(periods=1)
					g.forecast = g.pf.predict(future)
					g.predictionPrice = g.forecast['yhat'][0]

					# Assimilation
					if g.price[0] == None:
						g.price[0] = g.lastPrice
						g.price[1] = g.price[0]
						g.yhat[0] = g.predictionPrice
						g.yhat[1] = g.yhat[0]
					else:
						g.price[1] = g.price[0]
						g.price[0] = g.lastPrice
						g.yhat[1] = g.yhat[0]
						g.yhat[0] = g.predictionPrice

						# Crossover Logic
						g.isBearishChange = g.price[1] > g.yhat[1] and g.price[0] < g.yhat[0]
						g.isBullishChange = g.price[1] < g.yhat[1] and g.price[0] > g.yhat[0]

					# Trend
					g.isBearish = g.yhat[0] > g.price[0]
					g.isBullish = g.yhat[0] < g.price[0]

					# Signals
					if g.isBullishChange:
						g.currentSignal = 'buy'
						b = 500
						while b <= 5000:
							if os.name == 'posix':
								os.system('beep -f ' + str(b) + ' -l 50')
							b += 500
					if g.isBearishChange:
						g.currentSignal = 'sell'
						b = 5000
						while b >= 500:
							if os.name == 'posix':
								os.system('beep -f ' + str(b) + ' -l 50')
							b -= 500

					#################
					# End of analysis

					time.sleep(g.timeframe - 30)
					continue # In order to be timeframe agnostic we must cycle each analysis according to given seconds per bar.

				except (IndexError, TypeError, websocket.WebSocketException) as e:
					g.isConnected =  False
				#except:
				#	pass
				
		time.sleep(g.HIGH_PRIORITY_MS)