import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

class Send_Client:
	ws = None
	def on_message(ws, message):
		print(message)

	def on_error(ws, error):
		print(error)

	def on_close(ws):
		print("### closed ###")

	def on_open(ws):
		ws.send_test()

	def send_test(ws):
		def run(*args):
			for i in range(3):
				time.sleep(1)
				ws.ws.send("Hello %d" % i)
			time.sleep(1)
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

wsc = Send_Client("192.168.0.17:1880", "receiveMessage")
