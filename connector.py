from termcolor import colored
import os
import json
import websocket
import time
import globals as g

def connect():
	while not g.is_connected:
		os.system(g.clsstr)
		print('Connecting...', end=' ')
		try:
			g.iqoapi.connect()
			print(colored('OK', 'green'))
			g.is_connected = True
			b = 2000
			while b <= 10000:
				if os.name == 'posix':
					os.system('beep -f ' + str(b) + ' -l 100')
				b += 2000
		except (json.JSONDecodeError, websocket.WebSocketException, AttributeError) as e:
			print(colored('Connection Error, Retry', 'red'))
			time.sleep(3)
		except:
			print(colored('Unknown Error, Abort', 'red'))
			exit()

def connection():
	while True:
		try:
			g.is_connected = g.iqoapi.check_connect()
			if not g.is_connected:
				g.iqoapi.connect()
		except:
			continue
		time.sleep(g.LOW_PRIORITY_MS)