import unittest

from sosi_crawler_executor.crawler import Executor

class test_executor_execute_method(unittest.TestCase):
    """
    Test class responsible to perform tests routines against "execute" method
    """
    def test_should_raise_exception_for_missing_dependencies(self):
        """
        Should raise an exception for missing dependencies
        """
        try:
            Executor('tests/dependecies_missing.json', 'tests/executor_config.json').execute()
            pass
        except Exception as ex:
            self.assertTrue(str(ex).__contains__('is required. This crawler cannot run'))
            pass 
        pass
    pass

    def test_should_raise_exception_for_missing_configuration(self):
        """
        
        """
        try:
            Executor('tests/dependecies_config_reader_none_value.json', 'tests/executor_config_missing.json').execute()
            pass
        except Exception as ex:
            self.assertTrue(str(ex).__contains__('must be provided'))
            pass 
        pass
    pass
