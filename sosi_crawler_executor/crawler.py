from sosi_crawler_interfaces.IApiController import IApiController
from sosi_crawler_interfaces.IConfiguration import IConfiguration
from sosi_crawler_interfaces.ICrawler import ICrawler
from sosi_crawler_interfaces.ICrawlingResult import ICrawlingResult
from sosi_crawler_interfaces.IException import IException
from sosi_crawler_interfaces.ILogging import ILogging
from sosi_crawler_interfaces.IObjectFactory import IObjectFactory
from sosi_crawler_object_factory.factory import ObjectFactory

class Executor():
    """
    Class representing a crawler executor. 
    This class is responsible to handle all duties in terms of crawler's pre- & post-execution  
    """

    ## Global variables
    __object_factory: IObjectFactory = None
    __crawler: ICrawler = None
    __api_controller: IApiController = None
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
    __CONFIG_FILE_FIELD_DEST_URL: str = 'dest_url'
    __CONFIG_FILE_FIELD_CRAWLER_ARGS: str = 'crawler_args'
    __CONFIG_FILE_FIELD_CRAWLER_SERVICE_HEADER: str = 'service_header'
    __CONFIG_FILE_FIELD_SERVICE_EXT_ARGS: str = 'service_extra_args'
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
        self.__api_controller = self.__object_factory.get_instance(self.__class__.__name__, IApiController)
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
            destination_url: str = self.__configuration.read(self.__CONFIG_FILE_FIELD_DEST_URL)
            crawling_args: dict = self.__configuration.read(self.__CONFIG_FILE_FIELD_CRAWLER_ARGS)
            post_service_header: dict = self.__configuration.read(self.__CONFIG_FILE_FIELD_CRAWLER_SERVICE_HEADER)
            post_service_ext_params: dict = self.__configuration.read(self.__CONFIG_FILE_FIELD_SERVICE_EXT_ARGS)

            if destination_url is None or destination_url == '':
                self.__exception.manage_exception(self.__MSG_PARAM_MUST_BE_PROVIDED.format(self.__CONFIG_FILE_FIELD_DEST_URL), True)
            
            if crawling_args is None or crawling_args == '':
                self.__exception.manage_exception(self.__MSG_PARAM_MUST_BE_PROVIDED.format(self.__CONFIG_FILE_FIELD_CRAWLER_ARGS), True)
            
            if post_service_header is None or post_service_header == '':
                self.__exception.manage_exception(self.__MSG_PARAM_MUST_BE_PROVIDED.format(self.__CONFIG_FILE_FIELD_CRAWLER_SERVICE_HEADER), True)

            self.__logging.Log("Crawling has started")
            result: ICrawlingResult = self.__crawler.execute(crawling_args)
            
            if result is None:
                self.__exception.manage_exception("Crawling result cannot be null", True)
                            
            result_obj: dict = result.get_object()

            if result_obj is None:
                self.__exception.manage_exception("Crawling result object cannot be null", True)
                
            self.__logging.Log("Posting result to {0}".format(destination_url))
            self.__api_controller.post(destination_url, post_service_header, result_obj, post_service_ext_params)

            self.__logging.log("DONE HERE! :)")
        except Exception as ex:
            self.__exception.manage_exception(ex)

    def check_required_dependencies(self):
        """
        Check whether the required dependencies are instantiated or not
        """
        self.check_concrete_obj_is_none(self.__exception, type(IException).__class__.__name__)
        self.check_concrete_obj_is_none(self.__crawler, type(ICrawler).__class__.__name__)
        self.check_concrete_obj_is_none(self.__logging, type(ILogging).__class__.__name__)
        self.check_concrete_obj_is_none(self.__crawling_result, type(ICrawlingResult).__class__.__name__)
        self.check_concrete_obj_is_none(self.__configuration, type(IConfiguration).__class__.__name__)
        self.check_concrete_obj_is_none(self.__api_controller, type(IApiController).__class__.__name__)

        self.__logging.Log(self.__MSG_LOADED_OBJECT_MSG.format(type(self.__crawler), type(ICrawler).__class__.__name__))
        self.__logging.Log(self.__MSG_LOADED_OBJECT_MSG.format(type(self.__api_controller), type(IApiController).__class__.__name__))
        self.__logging.Log(self.__MSG_LOADED_OBJECT_MSG.format(type(self.__configuration), type(IConfiguration).__class__.__name__))
        self.__logging.Log(self.__MSG_LOADED_OBJECT_MSG.format(type(self.__crawling_result), type(ICrawlingResult).__class__.__name__))
        self.__logging.Log(self.__MSG_LOADED_OBJECT_MSG.format(type(self.__exception), type(IException).__class__.__name__))
        self.__logging.Log(self.__MSG_LOADED_OBJECT_MSG.format(type(self.__logging), type(ILogging).__class__.__name__))

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
