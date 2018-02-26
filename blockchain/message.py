import struct
import socket
import time
import random
from hashlib import sha256
from utils import net as u
from utils import byte as b
import binascii
import sys

def read_message(sock):
	resp_header = sock.recv(24)
	sb = b.ObjectIO()
	_, msg, length, checksum = struct.unpack("<I 12s I I", resp_header)

	total = length

	while total > 0:
		remain = total if total < 8096 else 8096
		income = sock.recv(remain)
		sb.write(income)
		total = total - len(income)
		print('Recieve: %d/%d'%(length - total, length))

	sb.seek(0)
	print('<-- (%s) %s %d' % (msg, binascii.hexlify(resp_header), length))
	return msg, sb

class Message(object):
	def __init__(self):
		''' Megic, command, length, checksum '''
		self.s = struct.Struct('I 12s I 4s')
		# 70 69 6e 67 00 00 00 00 00 00 00 00

	def make_message(self, command, payload):
		m = bytearray()
		header = bytes(self.s.pack(0xD9B4BEF9, command, len(payload),self.checksum(payload)))
		m.extend(header)
		if len(payload):
			m.extend(payload)
		
		return m

	def checksum(self, payload):
		return sha256(sha256(payload).digest()).digest()


	def handle_exception(self, msg, resp):
		pass

class Ping(Message):
	def __init__(self, *args, **kwargs):
		self.name = 'ping'
		super(Ping, self).__init__(*args, **kwargs)

	def request(self):
		return self.make_message('ping', struct.pack('<Q', random.getrandbits(8)))

	def read(self, payload):
		self.nonce = payload.read()

	def response(self):
		 msg = Pong()
		 msg.nonce = self.nonce
		 return msg

class Pong(Message):
	def __init__(self, *args, **kwargs):
		self.name = 'pong'
		self.nonce = None
		super(Pong, self).__init__(*args, **kwargs)

	def request(self):
		return self.make_message('pong', self.nonce)

	def read(self, resp):
		pass

	def response(self):
		pass


class Version(Message):
	def __init__(self, *args, **kwargs):
		self.name = 'version'
		super(Version, self).__init__(*args, **kwargs)

	def request(self):
		''' Version, Services, Timestamp, addr_recv, addr_from, nonce, user_agent, start_height, relay '''
		addr_me = u.ipv4_addr(socket.inet_aton(u.get_ip()), 8333, 1)
		addr_you = u.ipv4_addr(socket.inet_aton(u.get_ip()), 8333, 1)
		sub_version = ''
		payload = struct.pack('< L Q Q 26s 26s Q s I c', 60002, 1, int(time.time()), addr_me, addr_you, random.getrandbits(64), sub_version, 0, '\0')
		return self.make_message('version', payload)
	
	def read(self, resp):
		pass

	def response(self):
		pass

class Verack(Message):
	def __init__(self, *args, **kwargs):
		self.name = 'verack'
		super(Verack, self).__init__(*args, **kwargs)

	def request(self):
		return self.make_message('verack', '')
	
	def read(self, resp):
		pass

	def response(self):
		pass

class Addr(Message):
	def __init__(self, *args, **kwargs):
		self.name = 'addr'
		super(Addr, self).__init__(*args, **kwargs)

	def request(self):
		pass

	def read(self, resp):
		len = resp.read_var_int()
		print 'len: %d' % len
		for i in xrange(0, len):
			# print 'timestamp: {}'.format(resp.read_unix_time().strftime('%Y-%m-%d %H:%M:%S'))
			resp.read_int()
			resp.read_long()
			ip = resp.read_string(16)
			port = resp.read_short_big()
			print('addr: %s:%d' % (binascii.hexlify(ip), port))

	def response(self):
		pass

class GetAddr(Message):
	def __init__(self, *args, **kwargs):
		self.name = 'getaddr'
		super(GetAddr, self).__init__(*args, **kwargs)

	def request(self):
		return self.make_message(self.name, '')

	def response(self, resp):
		pass

class GetHeaders(Message):
	def __init__(self, *args, **kwargs):
		self.name = 'getheader'
		super(GetHeaders, self).__init__(*args, **kwargs)

	def request(self):
		return ''

	def read(self, resp):
		pass

	def response(self):
		pass

