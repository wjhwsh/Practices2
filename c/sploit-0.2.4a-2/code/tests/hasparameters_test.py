from interfaces.hasparameters import HasParameters, Parameter, StringParam, IntParam, KeyListParam
from interfaces.testcase import TestCase
from interfaces.testcase import Fail


class Foo(HasParameters):
	pass

class test_1(TestCase):
	def __init__(self):
		TestCase.__init__(self, "Parameters")
		
	def test_single_value_param(self):
		temp = Parameter("param0", 5, "desc0", False)
		if temp.get_value()!=5: raise Fail("Constuctor error")
		if temp.validate(8) != 8: raise Fail("Validation Fails")
		if temp.is_multi_values(): raise Fail("Is a multi-value")
		temp.set_value(44)
		if temp.get_value()!=44: raise Fail("set-get value")
		temp.set_value("bar")
		if temp.get_value()!="bar": raise Fail("set-get value")
		temp.reset()
		if temp.get_value()!=5: raise Fail("reset failed")
		temp.set_multiple_values([1,2,3])
		if temp.get_multiple_values()!=None: raise Fail("get_multiple_values not None")

	def test_multi_value_param(self):
		temp = Parameter("param0", 5, "desc0", True)
		if temp.validate(8) != 8: raise Fail("Validation Fails")
		if temp.is_multi_values()==False: raise Fail("Is not a multi-value")
		temp.set_value(44)
		if temp.get_value()!=44: raise Fail("set-get value")
		temp.set_value("bar")
		if temp.get_value()!="bar": raise Fail("set-get value")
		temp.reset()
		if temp.get_value()!=5: raise Fail("reset failed")
		temp.set_multiple_values([1,2,3])
		if temp.get_multiple_values()!=[1,2,3]: raise Fail("get_multiple_values failed")
		if temp.get_value()!=5: raise Fail("current value after multiple set")
		
	def test_string_param(self):
		temp = StringParam("param0", 5, "desc0", True)
		if temp.get_value()!="5": raise Fail("constuctor error")
		temp.set_multiple_values(["ciao",2,[]])
		if temp.get_multiple_values()!=["ciao","2","[]"]: raise Fail("get_multiple_values failed")
		
	def test_int_param(self):
		temp = IntParam("param0", 5, "desc0", 0, 10, True)
		try:
			temp.set_value(-1)
		except:
			pass
		else:
			raise Fail("boundary check failure")
			
		try:
			temp.set_value(11)
		except:
			pass
		else:
			raise Fail("boundary check failure")
		
		try:
			temp.set_value(11.3)
		except:
			pass
		else:
			raise Fail("type check failure")
		
		try:
			temp.set_value(0)
		except:
			raise Fail("boundary check failure")		
	
	def test_keylist_param(self):
		klist = [1,2,"ciao"]
		try:
			temp = KeyListParam("param0", 5, klist, "desc0", True)
		except:
			pass
		else:
			raise Fail("default value not in keylist")
			
		temp = KeyListParam("param0", 1, klist, "desc0", True)
		temp.set_value("ciao")
		if temp.get_value()!="ciao": raise Fail("correct set_value")
		try:
			temp.set_value(False)
		except:
			pass
		else:
			raise Fail("incorrect set_value")
		temp.set_multiple_values(klist)
		if temp.get_multiple_values()!=klist: raise Fail("get_multiple_values failed")


class test_2(TestCase):
	def __init__(self):
		TestCase.__init__(self, "HasParameter")
	def test_parameter(self):
		foo = Foo()
		if  foo.get_parameters_names()!=[]:  raise Fail("should be empty")	
		
		foo.add_param(StringParam("first", "ciao", "param1", True))
		if foo.first!="ciao": raise Fail("cannot add a parameter")
		foo.first = 7
		if foo.first!="7": raise Fail("cannot set a value")
		foo.add_param(IntParam("second", 6, "param2"))
		
		if foo.get_parameters_names() != ["second","first"]:  raise Fail("get_parameters_names")
		if foo.get_parameter("first").get_value() != "7": raise Fail("get_parameter")
		if len(foo.get_parameters()) != 2: raise Fail("get_parameters")
		
		foo.second = 100
		del foo.second
		if foo.second != 6: raise Fail("del does not reset")

	def test_param_combination(self):
		foo = Foo()
		foo.add_param(StringParam("first", "ciao", "param1", True))
		foo.set_multiple_values("first", ["a","b","c","d"])
		foo.add_param(IntParam("second", 6, "param2"))
		foo.add_param(StringParam("third", "f", "param3", True))
		foo.set_multiple_values("third", ["f","g","h"])
		
		if foo.params_combinations() != 12: raise Fail("combinations number")
		
		foo.set_params_combination(5)
		if foo.second != 6 or foo.first != "b" or foo.third != "h":
			raise Fail("wrong params combinations")
		
		temp = []
		for i in range(12):
			foo.set_params_combination(-1*i)
			values = [foo.first, foo.second, foo.third]
			if values in temp: 
				raise Fail("duplicate combination")
			temp.append(values)
			
		try:
			foo.set_params_combination(100)
		except IndexError:
			pass
		else:
			raise Fail("out of range combination")
		
		foo.add_param(IntParam("last", 0, "param4", 0, 100, True))
		foo.set_multiple_values("last", range(50))
		
		foo.set_params_combination(300)
			
		if foo.params_combinations() != 600: raise Fail("combinations number 2")




TESTS = [test_1(), test_2()]

