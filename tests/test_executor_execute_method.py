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

    def test_should_raise_exception_for_missing_destination_url(self):
        """
        
        """
        try:
            Executor('tests/dependecies_configuration_missing_param.json', 'dest_url').execute()
            pass
        except Exception as ex:
            self.assertTrue(str(ex).__eq__('The param "dest_url" must be provided'))
            pass 
        pass
    pass

    def test_should_raise_exception_for_missing_crawling_args(self):
        """
        
        """
        try:
            Executor('tests/dependecies_configuration_missing_param.json', 'crawler_args').execute()
            pass
        except Exception as ex:
            self.assertTrue(str(ex).__eq__('The param "crawler_args" must be provided'))
            pass 
        pass
    pass

    def test_should_raise_exception_for_missing_post_service_header(self):
        """
        
        """
        try:
            Executor('tests/dependecies_configuration_missing_param.json', 'service_header').execute()
            pass
        except Exception as ex:
            self.assertTrue(str(ex).__eq__('The param "service_header" must be provided'))
            pass 
        pass
    pass