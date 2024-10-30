import json
import os
import time
import websocket
from termcolor import cprint

from globals import Globals

class Connection():

	def run():
		while True:
			time.sleep(Globals.NORMAL_PRIORITY_MS)

			try:
				Globals.is_connected = Globals.iqoapi.check_connect()
				if not Globals.is_connected:
					Globals.iqoapi.connect()
			except:
				Globals.is_connected = False
    
	@staticmethod
	def connect():
		while not Globals.is_connected:
			os.system(Globals.clsstr)
			cprint('Connecting...', end=' ')
			try:
				Globals.iqoapi.connect()
				cprint('OK', 'light_green')
				Globals.is_connected = True
			except (json.JSONDecodeError, websocket.WebSocketException, AttributeError) as e:
				cprint('Connection Error, Retry', 'light_red')
				time.sleep(Globals.NORMAL_PRIORITY_MS)
			except (Exception) as e:
				cprint('Unknown Error, Abort', 'light_red')
				cprint(e.msg)
				exit()
