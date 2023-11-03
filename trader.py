import time
import globals as g

def trader():
	tradeData = []
	while True:
		if g.instrumentAllowed and not 'none' in g.currentSignal:
			try:
				tradeData = g.iqoapi.buy_order(g.INSTRUMENTS[g.PAIR]['TYPE'], g.INSTRUMENTS[g.PAIR]['ID'], g.currentSignal, g.entryAmount, g.INSTRUMENTS[g.PAIR]['LEVERAGE'], 'market', None, None, 'percent', g.STOP_LOSS_PERCENT, 'percent', g.TAKE_PROFIT_PERCENT, g.USE_TRAIL_STOP)
				if not tradeData[0]:
					time.sleep(g.LOW_PRIORITY_MS)
					continue
				g.ongoingTrades += 1
				g.lastSignal = g.currentSignal
				g.currentSignal = 'none'
				
				while True:
					time.sleep(g.HIGH_PRIORITY_MS)
					try:
						pData = g.iqoapi.get_position(tradeData[1])
						if pData[1]['position']['status'] == 'closed':
							break
						else:
							aData = g.iqoapi.get_async_order(tradeData[1])
							g.realTimePnl = aData['position-changed']['msg']['pnl']
						
						if g.currentSignal != 'none':
							if g.currentSignal is not g.lastSignal:
								g.iqoapi.close_position(tradeData[1])
					except:
						continue
				if float(pData[1]['position']['pnl_realized']) >= 0.00: g.totalWin += 1
				else: g.totalLoss += 1
				g.sessionBalanceStatus += float(pData[1]['position']['pnl_realized'])
				g.totalMadeEntries += 1
				g.ongoingTrades -= 1	
			except:
				time.sleep(g.LOW_PRIORITY_MS)
				continue
		time.sleep(g.HIGH_PRIORITY_MS)