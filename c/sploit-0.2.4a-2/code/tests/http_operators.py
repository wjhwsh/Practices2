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
		
		def test_no_mutation(self):
			self._run_test("tests/http-ops/http0.conf -v %s --noredirect -q -p random -r 0"%self.log_lvl)
		
		def test_fake_dir(self):
			self._run_test("tests/http-ops/http1.conf -v %s --noredirect -q -p random -r 0"%self.log_lvl)
		
		def test_begin_characters(self):
			self._run_test("tests/http-ops/http2.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)
			
		def test_cmd2url(self):
			self._run_test("tests/http-ops/http3.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)
			
		def test_header_case(self):
			self._run_test("tests/http-ops/http4.conf -v %s --noredirect -q -p random -r 0"%self.log_lvl)
			
		def test_malformed_request(self):
			self._run_test("tests/http-ops/http5.conf -v %s --noredirect -q -p random -r 0"%self.log_lvl)

		def test_multiple_slash(self):
			self._run_test("tests/http-ops/http6.conf -v %s --noredirect -q -p random -r 0"%self.log_lvl)
	
		def test_null_method(self):
			self._run_test("tests/http-ops/http7.conf -v %s --noredirect -q -p random -r 0"%self.log_lvl)
	
		def test_parameter_hiding(self):
			self._run_test("tests/http-ops/http8.conf -v %s --noredirect -q -p random -r 0"%self.log_lvl)

		def test_premature_ending(self):
			self._run_test("tests/http-ops/http9.conf -v %s --noredirect -q -p random -r 0"%self.log_lvl)
	
		def test_self_reference(self):
			self._run_test("tests/http-ops/http10.conf -v %s --noredirect -q -p random -r 0"%self.log_lvl)

		def test_slash2backslash(self):
			self._run_test("tests/http-ops/http11.conf -v %s --noredirect -q -p random -r 0"%self.log_lvl)

		def test_bad_slash_hex_enc(self):
			self._run_test("tests/http-ops/http12.conf -v %s --noredirect -q -p random -r 0"%self.log_lvl)

		def test_url_hex_enc(self):
			self._run_test("tests/http-ops/http13.conf -v %s --noredirect -q -p random -r 0"%self.log_lvl)
		
		def test_params_selfref(self):
			self._run_test("tests/http-ops/http14.conf -v %s --noredirect -q -p random -r 0"%self.log_lvl)
		
		def test_params_slash2backslash(self):
			self._run_test("tests/http-ops/http15.conf -v %s --noredirect -q -p random -r 0"%self.log_lvl)
		
		def test_weird_version(self):
			self._run_test("tests/http-ops/http16.conf -v %s --noredirect -q -p random -r 0"%self.log_lvl)

		def test_url2version(self):
			self._run_test("tests/http-ops/http17.conf -v %s --noredirect -q -p random -r all"%self.log_lvl)


TESTS = [AttackTest("HTTP operators", False)]
