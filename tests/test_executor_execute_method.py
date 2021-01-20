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

    def test_should_raise_exception_for_missing_msg_queue_target_error_topic(self):
        """
        Should raise exception given a missing "Error Topic" parameter (empty or none)
        """
        try:
            Executor('tests/dependecies_configuration_missing_param.json', 'msg_queue_target_error_topic').execute()
            pass
        except Exception as ex:
            self.assertTrue(str(ex).__eq__('The param "msg_queue_target_error_topic" must be provided'))
            pass 
        pass
    pass

    def test_should_raise_exception_for_missing_msg_queue_target_topic(self):
        """
        Should raise exception given a missing "Target Topic" parameter (empty or none)
        """
        try:
            Executor('tests/dependecies_configuration_missing_param.json', 'msg_queue_target_topic').execute()
            pass
        except Exception as ex:
            self.assertTrue(str(ex).__eq__('The param "msg_queue_target_topic" must be provided'))
            pass 
        pass
    pass

    def test_should_raise_exception_for_missing_crawling_args(self):
        """
        Should raise exception given a missing "Crawling Args" parameter (empty or none)
        """
        try:
            Executor('tests/dependecies_configuration_missing_param.json', 'crawling_args').execute()
            pass
        except Exception as ex:
            self.assertTrue(str(ex).__eq__('The param "crawler_args" must be provided'))
            pass 
        pass
    pass

    def test_should_raise_exception_for_none_crawler_result_obj(self):
        """
        
        """
        try:
            Executor('tests/dependecies_none_crawler_result_obj.json', 'tests/executor_config.json').execute()
            pass
        except Exception as ex:
            self.assertTrue(str(ex).__eq__('Crawling result cannot be null'))
            pass 
        pass
    pass

    def test_should_execute_crawler_successfully_not_posting_to_service(self):
        """
        
        """
        try:
            Executor('tests/dependecies_result_status_false.json', 'tests/executor_config.json').execute()
            pass
        except Exception as ex:
            self.assertTrue(False)
            pass 
        pass
    pass

    def test_should_execute_crawler_successfully_posting_to_service(self):
        """
        
        """
        try:
            Executor('tests/dependecies.json', 'tests/executor_config.json').execute()
            pass
        except Exception as ex:
            self.assertTrue(False)
            pass 
        pass
    pass