from sosi_crawler_interfaces.IException import IException
from sosi_crawler_interfaces.IApiController import IApiController
from sosi_crawler_interfaces.IConfiguration import IConfiguration
from sosi_crawler_interfaces.ICrawler import ICrawler
from sosi_crawler_interfaces.ICrawlingResult import ICrawlingResult
from sosi_crawler_interfaces.ILogging import ILogging
from sosi_crawler_interfaces.IDataRepository import IDataRepository
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
        return type('crawler_result', (ICrawlingResult,), {})

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
    dest_url: str = ""
    crawling_args: str = ""
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

        self.dest_url = 'teste'
        self.crawling_args = 'teste'
        self.service_header = 'teste'

        if(file_path == 'dest_url'):
            self.dest_url = ''
        elif(file_path == 'crawler_args'):
            self.crawling_args = ''
        elif(file_path == 'service_header'):
            self.service_header = ''

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

        if(field == 'dest_url'):
            return self.dest_url
        elif(field == 'crawler_args'):
            return self.crawling_args
        elif(field == 'service_header'):
            return self.service_header
        else:
            return default_value

class CrawlingResult(ICrawlingResult):
    """
    Generic class for Crawling Result
    """

    def __init__(self):
        super().__init__()

class ApiController(IApiController):
    """
    Generic class for Api Controller
    """

    def __init__(self):
        super().__init__()
    
    def post(self, url: str, header: object, data: object, param: Optional[object]) -> str:
        """
        Post data to an URL

        :param url: Target URL
        :param header: HTTP Headers
        :param data: Data to be sent to the target URL
        :param param: Extra parameters to be sent to the target server

        :type url: str
        :type header: object
        :type data: object
        :type param: Optional[object]

        :return: str
        """
        return "test-posted"

    def get(self, url: str, header: object, data: object, param: Optional[object]) -> str:
        """
        Get data from an URL

        :param url: Target URL
        :param header: HTTP Headers
        :param data: Data to be sent to the target URL
        :param param: Extra parameters to be sent to the target server

        :type url: str
        :type header: object
        :type data: object
        :type param: Optional[object]

        :return: str
        """
        return "test-gotten"

    def put(self, url: str, header: object, data: object, param: Optional[object]) -> str:
        """
        Put some data to an URL

        :param url: Target URL
        :param header: HTTP Headers
        :param data: Data to be sent to the target URL
        :param param: Extra parameters to be sent to the target server

        :type url: str
        :type header: object
        :type data: object
        :type param: Optional[object]

        :return: str
        """
        return "test-put"

    def delete(self, url: str, header: object, data: object, param: Optional[object]) -> str:
        """
        Delete data present into a repository (URL)

        :param url: Target URL
        :param header: HTTP Headers
        :param data: Data to be sent to the target URL
        :param param: Extra parameters to be sent to the target server

        :type url: str
        :type header: object
        :type data: object
        :type param: Optional[object]

        :return: str
        """
        return "test-deleted"