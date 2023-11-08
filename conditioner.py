import time
import websocket
from datetime import datetime

from PySide6.QtCore import QRunnable

from globals import Globals

class Conditioner(QRunnable):
    """
    Conditioner thread
    """

    def run(self):

        while True:
            microTime = int(datetime.now().strftime('%S'))
            if microTime == 35:
                try:
                    """sessionTime = int(datetime.now().strftime('%H'))
                    if not (sessionTime >= Globals.INSTRUMENTS[Globals.PAIR]['SESSION'][0] and sessionTime <
                            Globals.INSTRUMENTS[Globals.PAIR]['SESSION'][1]):
                        Globals.instrumentAllowed = False
                        continue"""

                    Globals.availableAssets = Globals.iqoapi.get_all_open_time()
                    if not Globals.availableAssets['turbo']['EURUSD']['open']:
                        Globals.instrumentAllowed = False
                        continue

                    """availableLeverage = Globals.iqoapi.get_available_leverages(Globals.INSTRUMENTS[Globals.PAIR]['TYPE'], Globals.INSTRUMENTS[Globals.PAIR]['ID'])
                    if not availableLeverage[1]['leverages'][0]['regulated'].count(Globals.INSTRUMENTS[Globals.PAIR]['LEVERAGE']) > 0:
                        Globals.instrumentAllowed = False
                        continue"""

                    Globals.instrumentAllowed = True
                    continue

                except (TypeError, websocket.WebSocketException) as e:
                    Globals.isConnected = False
                except:
                    Globals.instrumentAllowed = False
                    pass
            time.sleep(Globals.HIGH_PRIORITY_MS)
