from sosi_crawler_interfaces.IConfiguration import IConfiguration
from sosi_crawler_interfaces.ICrawler import ICrawler
from sosi_crawler_interfaces.ICrawlingResult import ICrawlingResult
from sosi_crawler_interfaces.IException import IException
from sosi_crawler_interfaces.ILogging import ILogging
from sosi_crawler_interfaces.IObjectFactory import IObjectFactory
from sosi_crawler_interfaces.IMessageQueue import IMessageQueue
from sosi_crawler_object_factory.factory import ObjectFactory

class Executor():
    """
    Class representing a crawler executor. 
    This class is responsible to handle all duties in terms of crawler's pre- & post-execution  
    """

    ## Global variables
    __object_factory: IObjectFactory = None
    __crawler: ICrawler = None
    __message_queue: IMessageQueue = None
    __configuration: IConfiguration = None
    __crawler: ICrawler = None
    __crawling_result: ICrawlingResult = None
    __exception: IException = None
    __logging: ILogging = None
    __crawler_config_file_path: str = ''

    ## Constant Values
    __MSG_LOADED_OBJECT_MSG: str = 'Object "{0}" loaded for "{1}"'
    __MSG_CONCRETE_OBJ_REQUIRED: str = 'A concrete object for "{0}" is required. This crawler cannot run'
    __MSG_PARAM_MUST_BE_PROVIDED: str = 'The param "{0}" must be provided'
    __CONFIG_FILE_FIELD_CRAWLER: str = 'crawler'
    __CONFIG_FILE_FIELD_MSG_QUEUE_TARGET_TOPIC: str = 'msg_queue_target_topic'
    __CONFIG_FILE_FIELD_MSG_QUEUE_TARGET_ERROR_TOPIC: str = 'msg_queue_target_error_topic'
    __CONFIG_FILE_FIELD_CRAWLER_ARGS: str = 'crawler_args'
    __MSG_INIT_PARAMS_REQUIRED: str = 'Path to dependencies and configuration files is required'

    def __init__(self, dependecies_file_path: str, crawler_config_file_path: str):
        """
        Class initializer

        :param dependecies_file_path: Path to JSON file indicating the dependencies that should handle the tasks before and after the crawler execution
        :param crawler_config_file_path: Path to JSON file that indicates the crawler configurations
        :type dependecies_file_path: str
        :type crawler_config_file_path: str     
        """
                
        super().__init__()
        
        if (dependecies_file_path is None or dependecies_file_path == '') or (crawler_config_file_path is None or crawler_config_file_path == ''):
            raise FileNotFoundError(self.__MSG_INIT_PARAMS_REQUIRED)
            
        self.__crawler_config_file_path = crawler_config_file_path

        self.__object_factory = ObjectFactory()
        self.__object_factory.load_dependencies(dependecies_file_path)

        self.__crawler = self.__object_factory.get_instance(self.__class__.__name__, ICrawler)
        self.__message_queue = self.__object_factory.get_instance(self.__class__.__name__, IMessageQueue)
        self.__configuration = self.__object_factory.get_instance(self.__class__.__name__, IConfiguration)
        self.__crawling_result = self.__object_factory.get_instance(self.__class__.__name__, ICrawlingResult)
        self.__exception = self.__object_factory.get_instance(self.__class__.__name__, IException)
        self.__logging = self.__object_factory.get_instance(self.__class__.__name__, ILogging)

    def execute(self):
        """
        Stats the crawling pipeline by runing the crawler
        """
           
        try:
            self.check_required_dependencies()
            self.__configuration.load(self.__crawler_config_file_path, self.__CONFIG_FILE_FIELD_CRAWLER)
            msg_queue_target_topic: str = self.__configuration.read(self.__CONFIG_FILE_FIELD_MSG_QUEUE_TARGET_TOPIC, None)
            msg_queue_target_error_topic: str = self.__configuration.read(self.__CONFIG_FILE_FIELD_MSG_QUEUE_TARGET_ERROR_TOPIC, None)     
            crawling_args: dict = self.__configuration.read(self.__CONFIG_FILE_FIELD_CRAWLER_ARGS, None)

            if msg_queue_target_topic is None or msg_queue_target_topic == '':
                self.__exception.manage_exception(self.__MSG_PARAM_MUST_BE_PROVIDED.format(self.__CONFIG_FILE_FIELD_MSG_QUEUE_TARGET_TOPIC), True)

            if msg_queue_target_error_topic is None or msg_queue_target_error_topic == '':
                self.__exception.manage_exception(self.__MSG_PARAM_MUST_BE_PROVIDED.format(self.__CONFIG_FILE_FIELD_MSG_QUEUE_TARGET_ERROR_TOPIC), True)
            
            if crawling_args is None or crawling_args == '':
                self.__exception.manage_exception(self.__MSG_PARAM_MUST_BE_PROVIDED.format(self.__CONFIG_FILE_FIELD_CRAWLER_ARGS), True)
            
            self.__logging.log("Crawling has started")
            result: ICrawlingResult = self.__crawler.execute(crawling_args)
            
            if result is None:
                self.__exception.manage_exception("Crawling result cannot be null", True)
                            
            result_obj: dict = result.get_object()
            result_msg: str = result.get_message()
            result_status: bool = result.get_crawling_status()

            self.__logging.log("Crawler message: " + result_msg)

            if result_status is True:            
                self.__logging.log("Publishing result to {0}".format(msg_queue_target_topic))
                self.__message_queue.publish(msg_queue_target_topic, result_obj)
            else:
                self.__logging.log(result_msg)
                self.__message_queue.publish(msg_queue_target_error_topic, result_obj)

            self.__logging.log("====== DONE HERE! :) ======")
        except Exception as ex:
            self.__exception.manage_exception(ex, True)

    def check_required_dependencies(self):
        """
        Check whether the required dependencies are instantiated or not
        """
        self.check_concrete_obj_is_none(self.__exception, IException.__name__)
        self.check_concrete_obj_is_none(self.__crawler, ICrawler.__name__)
        self.check_concrete_obj_is_none(self.__logging, ILogging.__name__)
        self.check_concrete_obj_is_none(self.__crawling_result, ICrawlingResult.__name__)
        self.check_concrete_obj_is_none(self.__configuration, IConfiguration.__name__)
        self.check_concrete_obj_is_none(self.__message_queue, IMessageQueue.__name__)

        self.__logging.log(self.__MSG_LOADED_OBJECT_MSG.format(type(self.__crawler), ICrawler.__name__))
        self.__logging.log(self.__MSG_LOADED_OBJECT_MSG.format(type(self.__message_queue), IMessageQueue.__name__))
        self.__logging.log(self.__MSG_LOADED_OBJECT_MSG.format(type(self.__configuration), IConfiguration.__name__))
        self.__logging.log(self.__MSG_LOADED_OBJECT_MSG.format(type(self.__crawling_result), ICrawlingResult.__name__))
        self.__logging.log(self.__MSG_LOADED_OBJECT_MSG.format(type(self.__exception), IException.__name__))
        self.__logging.log(self.__MSG_LOADED_OBJECT_MSG.format(type(self.__logging), ILogging.__name__))

    def check_concrete_obj_is_none(self, concrete_obj: object, expected_type_name: str):
        """
        Checks whether a concrete object is None or not. In case it's None, an exception should be raised

        :param concrete_obj: Concrete object
        :param expected_type_name: Expected type 
        :type concrete_obj: object
        :type expected_type_name: str        
        """
           
        if (concrete_obj is None) and (self.__exception is None):
            raise ValueError(expected_type_name)
        elif (concrete_obj is None):
            self.__exception.manage_exception(self.__MSG_CONCRETE_OBJ_REQUIRED.format(expected_type_name), True)
        else:
            return