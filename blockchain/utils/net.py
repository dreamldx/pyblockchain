import dns.resolver
import socket
import binascii
import struct
from cStringIO import StringIO
from io import BytesIO

def query_seed(domain):
	A = dns.resolver.query(domain, 'A')
	if len(A.response.answer) > 0:
		if len(A.response.answer[0]) >0:
			return A.response.answer[0][0].address
	return None

def ipv4_addr(ipv4, port, service):
	prefix = binascii.unhexlify('00000000000000000000FFFF')
	return struct.pack('<Q 12s 4s H', service, prefix, ipv4, port)
	# 00000000 0100000000000000 010000000000000000000000 7f0000018d2 0

def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip = s.getsockname()[0]
	s.close()

	return ip

class SocketClient(object):
	def __init__(self, ip, port, *args, **kwargs):
		super(SocketClient, self).__init__(*args, **kwargs)
		self.ip = ip
		self.port = port
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		

	def connect(self):
		self.s.connect((self.ip, self.port))
		print('connected to %s:%d' % (self.ip, self.port))

	def transaction(self, message):
		bin = message.request()
		print('--> (%s) %s' % (message.name, binascii.hexlify(bin)))
		self.s.send(bin)

class ObjectIO(BytesIO):
     _file_str = None

     def __init__(self):
         self._file_str = StringIO()

     def Append(self, str):
         self._file_str.write(str)

     def __str__(self):
         return self._file_str.getvalue()


