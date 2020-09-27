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
    __API_CONTROLLER_OBJ_NAME: str = 'concreteApiController'
    __CONFIGURATION_OBJ_NAME: str = 'concreteConfiguration'
    __CRAWLER_OBJ_NAME: str = 'concreteCrawler'
    __CRAWLING_RESULT_OBJ_NAME: str = 'concreteCrawlingResult'
    __EXCEPTION_OBJ_NAME: str = 'concreteException'
    __LOGGING_OBJ_NAME: str = 'concreteLogging'
    __LOADED_OBJECT_MSG: str = 'Object "{0}" loaded for "{1}"'
    __CONCRETE_OBJ_REQUIRED: str = 'A concrete object for "{0}" is required. This crawler cannot run'
    __PARAM_MUST_BE_PROVIDED: str = 'The param "{0}" must be provided'

    def __init__(self, dependecies_file_path: str, crawler_config_file_path: str):
        """

        """
                
        super().__init__()
        
        if (dependecies_file_path is None or dependecies_file_path == '') or (crawler_config_file_path is None or crawler_config_file_path == ''):
            raise FileNotFoundError("Path to dependencies and configuration files is required")

        self.__crawler_config_file_path = crawler_config_file_path

        self.__object_factory = ObjectFactory()
        self.__object_factory.load_dependencies(dependecies_file_path)

        self.__crawler = self.__object_factory.get_instance(self.__CRAWLER_OBJ_NAME, ICrawler)
        self.__api_controller = self.__object_factory.get_instance(self.__API_CONTROLLER_OBJ_NAME, IApiController)
        self.__configuration = self.__object_factory.get_instance(self.__CONFIGURATION_OBJ_NAME, IConfiguration)
        self.__crawling_result = self.__object_factory.get_instance(self.__CRAWLING_RESULT_OBJ_NAME, ICrawlingResult)
        self.__exception = self.__object_factory.get_instance(self.__EXCEPTION_OBJ_NAME, IException)
        self.__logging = self.__object_factory.get_instance(self.__LOGGING_OBJ_NAME, ILogging)

        self.__check_concrete_obj_is_none(self.__exception, type(IException).__class__.__name__)
        self.__check_concrete_obj_is_none(self.__crawler, type(ICrawler).__class__.__name__)
        self.__check_concrete_obj_is_none(self.__logging, type(ILogging).__class__.__name__)
        self.__check_concrete_obj_is_none(self.__crawling_result, type(ICrawlingResult).__class__.__name__)
        self.__check_concrete_obj_is_none(self.__configuration, type(IConfiguration).__class__.__name__)
        self.__check_concrete_obj_is_none(self.__api_controller, type(IApiController).__class__.__name__)

        self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__crawler), type(ICrawler).__class__.__name__))
        self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__api_controller), type(IApiController).__class__.__name__))
        self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__configuration), type(IConfiguration).__class__.__name__))
        self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__crawling_result), type(ICrawlingResult).__class__.__name__))
        self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__exception), type(IException).__class__.__name__))
        self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__logging), type(ILogging).__class__.__name__))

    def execute(self):
        """

        """
           
        try:
            self.__configuration.load(self.__crawler_config_file_path, 'SECTION_NAME')
            destination_url: str = self.__configuration.read('FIELD_URL')
            crawling_args: dict = self.__configuration.read('FIELD_ARGS')
            post_service_header: dict = self.__configuration.read('FIELD_HEAD')
            post_service_ext_params: dict = self.__configuration.read('FIELD_EXT_PARAMS')

            if destination_url is None or destination_url == '':
                self.__exception.manage_exception(self.__PARAM_MUST_BE_PROVIDED.format('FIELD_URL'), True)
            
            if crawling_args is None or crawling_args == '':
                self.__exception.manage_exception(self.__PARAM_MUST_BE_PROVIDED.format('FIELD_ARGS'), True)
            
            if post_service_header is None or post_service_header == '':
                self.__exception.manage_exception(self.__PARAM_MUST_BE_PROVIDED.format('FIELD_HEAD'), True)

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

    def __check_concrete_obj_is_none(self, concrete_obj: object, expected_type_name: str):
        """

        """
           
        if (concrete_obj is None) and (self.__exception is None):
            raise ValueError(expected_type_name)
        elif (concrete_obj is None):
            self.__exception.manage_exception(self.__CONCRETE_OBJ_REQUIRED.format(expected_type_name), True)
        else:
            return
