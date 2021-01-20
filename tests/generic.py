from sosi_crawler_interfaces.IException import IException
from sosi_crawler_interfaces.IApiController import IApiController
from sosi_crawler_interfaces.IConfiguration import IConfiguration
from sosi_crawler_interfaces.ICrawler import ICrawler
from sosi_crawler_interfaces.ICrawlingResult import ICrawlingResult
from sosi_crawler_interfaces.ILogging import ILogging
from sosi_crawler_interfaces.IDataRepository import IDataRepository
from sosi_crawler_interfaces.IMessageQueue import IMessageQueue
from typing import Optional

class CustomException(IException):
    """
    Generic Exception Class
    """
    def __init__(self):
        super().__init__()

    def manage_exception(self, ex: Exception, raise_exception: bool) -> str:
        raise AttributeError(str(ex))

class Log(ILogging):
    """
    Generic class for logging
    """

    def __init__(self):
        super().__init__()
    
    def _log_pipeline(self, message: str):
        """
        Add a commando to the log operation pipeline. It can be called many times along the log pipeline execution
        IMPORTANT: The method that over writes this one should only beresponsible to expose the log message to the end user

        :param messagem: A message to log
        :type message: str
        """ 
        print(message)

class Crawler(ICrawler):
    """
    Generic class for crawling
    """

    def __init__(self):
        super().__init__()
    
    def execute(self, args: dict) -> ICrawlingResult:
        """
        Main method for a crawling object

        :param args: Set of arguments needed to run the crawler object
        :type args: dict
        """

        return_value: ICrawlingResult = CrawlingResult()
        return_value.set_result("", True, {})

        return return_value
    
class CrawlerStatusFalse(ICrawler):
    """
    Generic class for crawling
    """

    def __init__(self):
        super().__init__()
    
    def execute(self, args: dict) -> ICrawlingResult:
        """
        Main method for a crawling object

        :param args: Set of arguments needed to run the crawler object
        :type args: dict
        """
        return CrawlingResult()

class CrawlerNoneResultObj(ICrawler):
    """
    Generic class for crawling
    """

    def __init__(self):
        super().__init__()
    
    def execute(self, args: dict) -> ICrawlingResult:
        """
        Main method for a crawling object

        :param args: Set of arguments needed to run the crawler object
        :type args: dict
        """
        return None

class Configuration(IConfiguration):
    """
    Generic class for configuration
    """

    def __init__(self):
        super().__init__()
    
    def load(self, file_path: str, section_name: str):
        """
        Loads in memory a configuration section from a given file path. 
        It's only accepted a JSON file as configuration file
        
        :param file_path: Configuration file path
        :param section_name: Section to be load by the configuration loader mechanism 
        :type file_path: str
        :type section_name: str
        :return: void
        """
        return

    def read(self, field: str, default_value: str = None) -> str: 
        """
        Read a field value within the in-memory configuration section.
        If either field or value are not found, the default value will be returned.

        :param field: Field name
        :param defaultValue: Default value to be returned in case either field or value are not present 
        :type field: str
        :type default_value: str
        :default default_value: None
        :return: str
        """
        return 'text'

class ConfigurationMissingParam(IConfiguration):
    """
    Generic class for configuration
    """
    msg_queue_target_topic: str = ""
    msg_queue_target_error_topic: str = ""
    service_header: str = ""

    def __init__(self):
        super().__init__()
    
    def load(self, file_path: str, section_name: str):
        """
        Loads in memory a configuration section from a given file path. 
        It's only accepted a JSON file as configuration file
        
        :param file_path: Configuration file path
        :param section_name: Section to be load by the configuration loader mechanism 
        :type file_path: str
        :type section_name: str
        :return: void
        """

        self.msg_queue_target_topic = 'msg_queue_target_topic'
        self.msg_queue_target_error_topic = 'msg_queue_target_error_topic'
        self.crawling_args = 'crawling_args'

        if(file_path == 'msg_queue_target_topic'):
            self.msg_queue_target_topic = ''
        elif(file_path == 'msg_queue_target_error_topic'):
            self.msg_queue_target_error_topic = ''
        elif(file_path == 'crawling_args'):
            self.crawling_args = ''

        return

    def read(self, field: str, default_value: str = None) -> str: 
        """
        Read a field value within the in-memory configuration section.
        If either field or value are not found, the default value will be returned.

        :param field: Field name
        :param defaultValue: Default value to be returned in case either field or value are not present 
        :type field: str
        :type default_value: str
        :default default_value: None
        :return: str
        """

        if(field == 'msg_queue_target_topic'):
            return self.msg_queue_target_topic
        elif(field == 'msg_queue_target_error_topic'):
            return self.msg_queue_target_error_topic
        elif(field == 'crawling_args'):
            return self.crawling_args
        else:
            return default_value

class CrawlingResult(ICrawlingResult):
    """
    Generic class for Crawling Result
    """

    def __init__(self):
        super().__init__()

class MessageQueue(IMessageQueue):
    """
    Generic class for Message Queue
    """

    def __init__(self):
        super().__init__()
    
    def publish(self, topic: str, message: dict):
        """
        Publish a message to a given topic

        :param topic: Target topic name
        :param message: Object representing the JSON message to be sent to the topic. NOTE: This will be parsed to JSON.
        :type topic: str
        :type message: dict
        """
        pass

    def consume(self, topic: str) -> dict:
        """
        Consume a message from a topic queue

        :param topic: Target topic name
        :type topic: str
        :return: dict
        """
        pass
    