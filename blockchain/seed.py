import io
import thread

from utils.net import SocketClient
from blockchain.message import Ping, Pong, Message, Version, Verack, GetAddr, Addr, GetHeaders
from blockchain.message import read_message

msg_map = {
	'ping': Ping(),
	'pong': Pong(),
	'version': Version(),
	'verack': Verack(),
	'getaddr': GetAddr(),
	'addr': Addr(),
	'getheaders': GetHeaders()
}

class Seed(SocketClient):
	def __init__(self, ip, port):
		self.ip = ip
		super(Seed,self).__init__(ip=ip, port=port)

	def __getattr__(self, item):
		def c():
			self.transaction(msg_map[item])
		return c

	def default(self, msg, resp):
		message = msg_map[msg.strip('\0')]
		message.read(resp)
		resp = message.response()
		if resp:
			self.transaction(resp)

	def start_listen_thread(self):
		def listen_thread(name):
			while True:
				msg, resp = read_message(self.s)
				self.default(msg, resp)
		thread.start_new_thread(listen_thread, ('listener thread',))

