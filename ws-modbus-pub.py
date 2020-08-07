import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
from random import seed
from random import randint

seed(1)

def get_rand():
	return randint(0, 50)

class Send_Client:
	ws = None
	def on_message(ws, message):
		print(message)

	def on_error(ws, error):
		print(error)

	def on_close(ws):
		print("*** closed ***")

	def on_open(ws):
		ws.send_test()

	def get_status(self, sens):
		return "%s,%s,%s,%s,%s"%(1, 5, 1, sens, 1)

	def send_test(ws):
		def run(*args):
			for i in range(400000):
				ws.ws.send(ws.get_status(i%4))
				ws.ws.send("%s,%s,%s,%s,%s"%(str(get_rand()), 6, 1, i%4, 1))
				time.sleep(0.001)
			time.sleep(0.001)
			ws.ws.close()
			print("thread terminating...")
		thread.start_new_thread(run, ())

	def __init__(self, ip, socket):
		ws_name = "ws://%s/ws/%s" % (ip, socket)
		websocket.enableTrace(True)
		self.ws = websocket.WebSocketApp(ws_name,
								on_message = self.on_message,
								on_error = self.on_error,
								on_close = self.on_close)
		self.ws.on_open = self.on_open
		self.ws.run_forever()

wsc = Send_Client("192.168.0.14:1880", "modbus/write")
