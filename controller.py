import time
import os
import threading
import websocket
from datetime import datetime
from termcolor import colored
import globals as g
import connector as c
import analyser as a
import trader as t

g.clsstr = ''
if os.name == 'posix':
	g.clsstr = 'clear'
elif os.name == 'nt':
	g.clsstr = 'cls'

c.connect()
g.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# SET BALANCE
g.iqoapi.change_balance(g.balanceType.upper())
#g.iqoapi.reset_practice_balance()

def _M_AccountBalance():
	simulatedAmount = 100
	isSimulated = True
	try:
		b = round(g.iqoapi.get_balance(), 2)
		if isSimulated: return float(b - (10000 - simulatedAmount))
		else: return float(round(g.iqoapi.get_balance(), 2))
	except:
		return 1

g.accountBalance = _M_AccountBalance()

# THREADED FUNCTIONS
def statistics():
	while True:
		if g.totalWin > 0: g.assertivityScore = round((g.totalWin / (g.totalWin + g.totalLoss)) * 100, 2)
		if g.assertivityScore > g.assertHigh: g.assertHigh = g.assertivityScore
		if g.assertLow == 0: g.assertLow =  g.assertivityScore
		if g.assertivityScore < g.assertLow: g.assertLow = g.assertivityScore
		if g.sessionBalanceStatus > g.sessionBalanceHigh: g.sessionBalanceHigh = g.sessionBalanceStatus
		if g.sessionBalanceStatus < g.sessionBalanceLow: g.sessionBalanceLow = g.sessionBalanceStatus
		g.accountBalance = _M_AccountBalance()
		time.sleep(g.LOW_PRIORITY_MS)

def interface():
	while True:
		os.system(g.clsstr)
		print(colored('Autoption', 'blue', None, ['bold']) + colored(' [for IQOption]', 'white', None, ['dark']))
		print('STime: ' + g.start_time + ' | CTime: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		print(colored('Connected', 'green')) if g.is_connected else print(colored('Disconnected', 'red'))
		print(colored('\tAssertiveness: ' + str(g.assertivityScore) + '% (High: ' + str(g.assertHigh) + '% / Low: ' + str(g.assertLow) + '%)', None, None, ['bold']) + ' @ M' + str(g.timeframe.denominator)) if g.assertivityScore > 0 else print(colored('\tAssertiveness: 0%', None, None, ['bold']) + ' @ M' + str(g.timeframe.denominator))
		print('\tP: ' + colored(str(g.totalWin), 'green') +' / L: ' + colored(str(g.totalLoss), 'red') + ' / T: ' + colored(str(g.totalMadeEntries), 'white', None, ['dark', 'bold']))
		print('\tConsolidated Profit: ' + colored('R$' + "{:.2f}".format(g.sessionBalanceStatus), 'green', None, ['bold']) + ' (High: ' + 'R$' + "{:.2f}".format(g.sessionBalanceHigh) + ' / Low: ' + 'R$' + "{:.2f}".format(g.sessionBalanceLow) + ')') if g.sessionBalanceStatus >= 0 else print('\tConsolidated Damage: ' + colored('R$' + "{:.2f}".format(abs(g.sessionBalanceStatus)), 'red', None, ['bold']) + ' (High: ' + 'R$' + "{:.2f}".format(g.sessionBalanceHigh) + ' / Low: ' + 'R$' + "{:.2f}".format(g.sessionBalanceLow) + ')')
		print('\t' + colored('R$' + "{:.2f}".format(g.accountBalance), 'green', None, ['bold']) + ' (' + g.balanceType + ') (' + "{:.2f}".format((g.entryAmount / g.accountBalance) * 100, 2) + '% Balance Risk)')
		print('\tInstrument: ' + colored(g.PAIR, 'yellow'), end='')
		if(g.lastPrice is not None):
			print(' - Last Price: ' + colored("{:.2f}".format(g.lastPrice), 'yellow', None, ['bold']), end='')
		if g.isBearish or g.isBullish:
			if g.isBullish:
				print(colored(' ▲ Uptrend', 'green', None, ['bold']), end = '')
			elif g.isBearish:
				print(colored(' ▼ Downtrend', 'red', None, ['bold']), end = '')
		if(g.predictionPrice is not None):
			print(' Prediction: ' + colored("{:.2f}".format(g.predictionPrice), 'magenta', None, ['bold']))
		#if(g.yhat[0] is not None):
			#print(' (RQKernel ' + colored("{:.2f}".format(g.forecastK), 'magenta', None, ['dark']), end='')
		#if(g.forecastP is not None):
			#print(' & Prophet ' + colored("{:.2f}".format(g.forecastP['yhat'][0]) , 'magenta', None, ['dark']) + ')')
			#fig = g.pf.plot(g.forecastP)
			#fig.show()

		if not g.is_connected:
			print(colored('\tWaiting Connection...', 'red', None, ['dark']))
		else:
			if g.instrumentAllowed:
				if g.ongoingTrades > 0:
					print('\tApprox. PnL: ' + colored('+R$' + str(g.realTimePnl)), 'green') if g.realTimePnl >= 0.00 else print('\tApprox. PnL: ' + colored('-R$' + str(abs(round(g.realTimePnl, 2))), 'red'))
				else:
					print(colored('\tSurfing Market...', 'cyan', None, ['bold']))
			else:
				print(colored('\tWaiting Clearance...', 'cyan', None, ['dark']))
		time.sleep(g.NORMAL_PRIORITY_MS)

def conditioner():
	while True:
		microTime = int(datetime.now().strftime('%S'))
		if microTime == 35:
			try:
				sessionTime = int(datetime.now().strftime('%H'))
				if not (sessionTime >= g.INSTRUMENTS[g.PAIR]['SESSION'][0] and sessionTime < g.INSTRUMENTS[g.PAIR]['SESSION'][1]):
					g.instrumentAllowed = False
					continue

				availableAssets = g.iqoapi.get_all_open_time()
				if not availableAssets[g.INSTRUMENTS[g.PAIR]['TYPE']][g.INSTRUMENTS[g.PAIR]['ID']]['open']:
					g.instrumentAllowed = False
					continue

				availableLeverage = g.iqoapi.get_available_leverages(g.INSTRUMENTS[g.PAIR]['TYPE'], g.INSTRUMENTS[g.PAIR]['ID'])
				if not availableLeverage[1]['leverages'][0]['regulated'].count(g.INSTRUMENTS[g.PAIR]['LEVERAGE']) > 0:
					g.instrumentAllowed = False
					continue
				
				g.iqoapi.start_candles_stream(g.INSTRUMENTS[g.PAIR]['ID'], g.timeframe, 1)
				cdl = g.iqoapi.get_realtime_candles(g.INSTRUMENTS[g.PAIR]['ID'], g.timeframe)
				g.iqoapi.stop_candles_stream(g.INSTRUMENTS[g.PAIR]['ID'], g.timeframe)
				for candleId in cdl:
					if (g.INSTRUMENTS[g.PAIR]['MAX_SPREAD'] != 0) or (round((cdl[candleId]['ask'] - cdl[candleId]['bid']) / (cdl[candleId]['ask'] / 100), 3) > g.INSTRUMENTS[g.PAIR]['MAX_SPREAD']):
						g.instrumentAllowed = False
						continue
					else:
						g.instrumentAllowed = True
						continue
				g.instrumentAllowed = True
				continue

			except (TypeError, websocket.WebSocketException) as e:
				g.isConnected =  False
			except:
				g.instrumentAllowed = False
				pass
		time.sleep(g.HIGH_PRIORITY_MS)

# LAUNCH MAIN THREADS
try:
	connectionThread = threading.Thread(target=c.connection, name='Connection Manager')
	statisticsThread = threading.Thread(target=statistics, name='Statistics Manager')
	interfaceThread = threading.Thread(target=interface, name='User Interface')
	conditionerThread = threading.Thread(target=conditioner, name='Instrument Conditioner')
	analyserThread = threading.Thread(target=a.analyse, name='Price Action Analyser')
	traderThread = threading.Thread(target=t.trader, name='Trader')
	connectionThread.start()
	statisticsThread.start()
	interfaceThread.start()
	conditionerThread.start()
	analyserThread.start()
	traderThread.start()
except:
	print(colored('Thread Error, Abort', 'red'))
	exit()
