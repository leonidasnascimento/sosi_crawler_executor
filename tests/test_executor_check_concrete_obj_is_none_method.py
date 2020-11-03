import unittest

from sosi_crawler_executor.crawler import Executor

class test_executor_check_concrete_obj_is_none_method(unittest.TestCase):
    """
    Test class responsible to perform tests routines against private method "check_concrete_obj_is_none"
    """

    def test_should_not_raise_exception(self):
        """
        
        """
        try:
            obj: Executor = Executor('tests/dependecies.json', 'crawler_obj')
            obj.check_concrete_obj_is_none('str_obj', type(str).__class__.__name__)
            
            self.assertTrue(True)
            pass
        except Exception as ex:
            self.assertTrue(str(ex).__eq__('Path to dependencies and configuration files is required'))
            pass   
        pass
    pass

    def test_should_raise_exception_through_custom_class(self):
        """
        
        """
        try:
            obj: Executor = Executor('tests/dependecies.json', 'crawler_obj')
            obj.check_concrete_obj_is_none(None, type(str).__class__.__name__)

            self.assertTrue(True)
            pass
        except AttributeError:
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)
        pass
    pass