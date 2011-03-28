# Author: Davide Balzarotti
# $Id: sploit 111 2006-03-01 20:29:47Z balzarot $

from interfaces.testcase import TestCase
from interfaces.testcase import Fail
import interfaces.exploit
import string
import sys
import sploit

error_string = None

test_cases = [["SimpleRequest", False, "tests/base_http_test.conf -v ERROR --noredirect -q -p random -r 0"],
			  ["SimpleRequest(with TCP/IP stack)", True, "tests/base_http_test2.conf -v ERROR --noredirect -q -p random -r 0"]
			 ]

def cback(number, info):
	if info.result != interfaces.exploit.RES_OK:
		error_string = "%d : %s"%(number, interfaces.exploit.results[info.result]) 
		return False
	return True

class AttackTest(TestCase):
		def __init__(self, name, root, params):
			TestCase.__init__(self, name, root)
			self.params = params

		def test_attack_execution(self):
			error_string = None
			cl = sploit.CLInterface()
			
			argv = string.split(self.params)
			
			if cl.parse_options(argv)== False:
				sys.exit(1)
			cl.set_callback(cback)
			cl.run()
			
			if error_string:
				raise Fail(error_string)
	
TESTS = []
i = 1
for n,r,t in test_cases:
	TESTS.append(AttackTest(n,r,t))
