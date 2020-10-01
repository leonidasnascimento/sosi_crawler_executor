import unittest

from sosi_crawler_executor.crawler import Executor

class test_executor_init_method(unittest.TestCase):
    """
    Test class responsible to perform tests routines against "__init__" method
    """

    def test_should_raise_exception_for_empty_dep_path_params(self):
        """
        Should raise an exception for empty "dependecies_file_path" param
        """
        try:
            Executor('', 'crawler_obj')
            pass
        except Exception as ex:
            self.assertTrue(str(ex).__eq__('Path to dependencies and configuration files is required'))
            pass   
        pass
    pass

    def test_should_raise_exception_for_empty_config_file_path_params(self):
        """
        Should raise an exception for empty "crawler_config_file_path" param
        """
        try:
            Executor('crawler_obj', '')
            pass
        except Exception as ex:
            self.assertTrue(str(ex).__eq__('Path to dependencies and configuration files is required'))
            pass   
        pass
    pass
