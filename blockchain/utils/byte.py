from io import BytesIO
import struct
import datetime
import binascii

class ObjectIO(BytesIO):
	def __init__(self, *args, **kwarg):
		super(ObjectIO, self).__init__(*args, **kwarg)

	def length(self):
		return self.__sizeof__()

	def read_byte(self): # 2 btyes
		data = self.read(1)
		return struct.unpack('<B', data)[0]

	def read_short(self): # 2 btyes
		data = self.read(2)
		return struct.unpack('<H', data)[0]

	def read_short_big(self): # 2 btyes
		data = self.read(2)
		return struct.unpack('>H', data)[0]

	def read_int(self):   # 4 btyes
		data = self.read(4)
		return struct.unpack('<I', data)[0]

	def read_long(self):  # 8 btyes
		data = self.read(8)
		return struct.unpack('<Q', data)[0]

	def read_boolean(self):
		data = self.read_byte()
		return data != 0

	def read_hex(self, n):
		return self.read_string(n)

	def read_string(self, n):
		data = self.read(n)
		return struct.unpack('!%ds' % n, data)[0]

	def read_var_int(self):
		data = ord(self.read(1))
		if data < 0xfd:
			return data
		elif data == 0xfd:
			return self.read_short()
		elif data == 0xfe:
			return self.read_int()
		elif data == 0xff:
			return self.read_long()

	def read_var_string(self):
		length = self.read_var_int()
		return self.read_string(length)

	def read_unix_time(self):
		unix_time = self.read_long()
		return datetime.datetime.fromtimestamp(unix_time)