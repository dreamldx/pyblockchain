import binascii
import socket
import time

import sys
sys.path.append('../utils')

from blockchain.utils.net import query_seed, get_ip
from blockchain.seed import Seed

ip = '194.14.246.74'
if ip:
	s = Seed(ip, 8333)
	s.start_listen_thread()
	s.connect()
	s.version()
	s.verack()
	s.ping()
	s.getaddr()

while True:
	time.sleep(5)

