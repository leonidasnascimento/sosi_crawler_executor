import unittest

from sosi_crawler_executor.crawler import Executor

class test_executer_initializer(unittest.TestCase):
    """
    docstring
    """

    def test_should_raise_exception_for_empty_init_params(self):
        """
        docstring
        """
        try:
            Executor('', 'crawler_obj')
            pass
        except Exception as ex:
            self.assertTrue(str(ex).__eq__('Path to dependencies and configuration files is required'))
            pass   
        pass
    pass
