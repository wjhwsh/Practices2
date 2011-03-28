# Author: Davide Balzarotti
# $Id: sploit 111 2006-03-01 20:29:47Z balzarot $

from interfaces.testcase import TestCase
from interfaces.testcase import Fail
import interfaces.exploit
import string
import sys
import sploit

error_string = None

def cback(number, info):
	global error_string
	if info.result != interfaces.exploit.RES_OK:
		error_string = "Mut. #%d: %s"%(info.number, interfaces.exploit.results[info.result]) 
		return False
	return True

class AttackTest(TestCase):
		def __init__(self, name, root):
			TestCase.__init__(self, name, root)
			self.log_lvl = "OFF"

		def _run_test(self, cmd_line):
			global error_string
			error_string = None
			cl = sploit.CLInterface()
			
			argv = string.split(cmd_line)
			
			if cl.parse_options(argv)== False:
				raise Fail("Cannot parse the option")
			cl.set_callback(cback)
			cl.run()
			
			if error_string:
				raise Fail(error_string)
		
		def test_without_mutations(self):
			self._run_test("tests/net-conf/echo_test_base.conf -v %s --noredirect -q -p random -r 0"%self.log_lvl)
		
		def test_fragmenter(self):
			self._run_test("tests/net-conf/echo_ip_1.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)
			
		def test_retarder(self):
			self._run_test("tests/net-conf/echo_ip_2.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)
			
		def test_retarder2(self):
			self._run_test("tests/net-conf/echo_ip_3.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)
			
		def test_duplicate(self):
			self._run_test("tests/net-conf/echo_ip_4.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)

		def test_out_of_order(self):
			self._run_test("tests/net-conf/echo_ip_5.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)
	
		def test_out_of_order2(self):
			self._run_test("tests/net-conf/echo_ip_6.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)
	
		def test_overlapped(self):
			self._run_test("tests/net-conf/echo_ip_7.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)

		def test_bad_chacksum(self):
			self._run_test("tests/net-conf/echo_ip_8.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)
	
		def test_bad_version(self):
			self._run_test("tests/net-conf/echo_ip_9.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)

		def test_bad_proto(self):
			self._run_test("tests/net-conf/echo_ip_10.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)

		def test_bad_optlength(self):
			self._run_test("tests/net-conf/echo_ip_11.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)

		def test_last_first(self):
			self._run_test("tests/net-conf/echo_ip_12.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)
		
		def test_short_ttl(self):
			self._run_test("tests/net-conf/echo_ip_13.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)
		
		def test_big_mtu(self):
			self._run_test("tests/net-conf/echo_ip_14.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)
		
		def test_bad_tot_length(self):
			self._run_test("tests/net-conf/echo_ip_15.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)

		def test_broadcast_syn(self):
			self._run_test("tests/net-conf/echo_ip_16.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)


class AttackTest2(TestCase):
		def __init__(self, name, root):
			TestCase.__init__(self, name, root)
			self.log_lvl = "OFF"

		def _run_test(self, cmd_line):
			global error_string
			error_string = None
			cl = sploit.CLInterface()
			
			argv = string.split(cmd_line)
			
			if cl.parse_options(argv)== False:
				raise Fail("Cannot parse the option")
			cl.set_callback(cback)
			cl.run()
			
			if error_string:
				raise Fail(error_string)
		
		
		def test_split(self):
			self._run_test("tests/net-conf/echo_tcp_1.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)
			
		def test_clear_ack(self):
			self._run_test("tests/net-conf/echo_tcp_2.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)

		def test_out_of_order2(self):
			self._run_test("tests/net-conf/echo_tcp_3.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)

		def test_bad_option(self):
			self._run_test("tests/net-conf/echo_tcp_4.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)

		def test_rst_fake_checksum(self):
			self._run_test("tests/net-conf/echo_tcp_5.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)

		def test_overlap(self):
			self._run_test("tests/net-conf/echo_tcp_6.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)

		def test_bad_checksum(self):
			self._run_test("tests/net-conf/echo_tcp_7.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)

		def test_bad_header_length(self):
			self._run_test("tests/net-conf/echo_tcp_8.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)

		def test_rst_bad_sequence(self):
			self._run_test("tests/net-conf/echo_tcp_9.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)

		def test_out_of_order(self):
			self._run_test("tests/net-conf/echo_tcp_10.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)

		def test_duplicate(self):
			self._run_test("tests/net-conf/echo_tcp_11.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)

		def test_bad_sequence(self):
			self._run_test("tests/net-conf/echo_tcp_12.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)

		def test_interleaved_syn(self):
			self._run_test("tests/net-conf/echo_tcp_13.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)

		#def test_bad_flags(self):
		#	self._run_test("tests/net-conf/echo_tcp_14.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)

		def test_retarder(self):
			self._run_test("tests/net-conf/echo_tcp_15.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)

		def test_syn_data(self):
			self._run_test("tests/net-conf/echo_tcp_16.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)

		def test_no_3wh(self):
			self._run_test("tests/net-conf/echo_tcp_17.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)

		def test_bad_packet_noack(self):
			self._run_test("tests/net-conf/echo_tcp_18.conf -v %s --noredirect -q --p random -r all"%self.log_lvl)



TESTS = [AttackTest("IP stack", True), AttackTest2("TCP stack", True)]
