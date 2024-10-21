import json
import os
import time
import websocket
from termcolor import cprint

from PySide6.QtCore import QThread

from globals import Globals

class Connection(QThread):

	def __init__(self):
		super().__init__()
		self.setObjectName('Connection Thread')

	def run(self):
		while True:
			try:
				Globals.is_connected = Globals.iqoapi.check_connect()
				if not Globals.is_connected:
					Globals.iqoapi.connect()
			except:
				Globals.is_connected = False
			time.sleep(Globals.NORMAL_PRIORITY_MS)
    
	@staticmethod
	def connect():
		while not Globals.is_connected:
			os.system(Globals.clsstr)
			cprint('Connecting...', end=' ')
			try:
				Globals.iqoapi.connect()
				cprint('OK', 'light_green')
				Globals.is_connected = True
				b = 2000
				while b <= 10000:
					if os.name == 'posix':
						os.system('beep -f ' + str(b) + ' -l 100')
					b += 2000
			except (json.JSONDecodeError, websocket.WebSocketException, AttributeError) as e:
				cprint('Connection Error, Retry', 'light_red')
				time.sleep(Globals.NORMAL_PRIORITY_MS)
			except (Exception) as e:
				cprint('Unknown Error, Abort', 'light_red')
				cprint(e.msg)
				exit()
