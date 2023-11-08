import json
import os
import time
import websocket
from termcolor import colored

from PySide6.QtCore import QRunnable

from globals import Globals

class Connection(QRunnable):
    
	@staticmethod
	def connect():
		while not Globals.is_connected:
			os.system(Globals.clsstr)
			print('ConnectinGlobals...', end=' ')
			try:
				Globals.iqoapi.connect()
				print(colored('OK', 'green'))
				Globals.is_connected = True
				b = 2000
				while b <= 10000:
					if os.name == 'posix':
						os.system('beep -f ' + str(b) + ' -l 100')
					b += 2000
			except (json.JSONDecodeError, websocket.WebSocketException, AttributeError) as e:
				print(colored('Connection Error, Retry', 'red'))
				print(e.msg)
				time.sleep(3)
			except (Exception) as e:
				print(colored('Unknown Error, Abort', 'red'))
				print(e.msg)
				exit()


	def run(self):
		while True:
			try:
				Globals.is_connected = Globals.iqoapi.check_connect()
				if not Globals.is_connected:
					Globals.iqoapi.connect()
			except:
				continue
			time.sleep(Globals.LOW_PRIORITY_MS)
