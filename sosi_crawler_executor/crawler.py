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
    __dep_file_path: str = ''
    __crawler_config_file_path: str = ''

    ## Constant Values
    __API_CONTROLLER_OBJ_NAME: str = 'concreteApiController'
    __CONFIGURATION_OBJ_NAME: str = 'concreteConfiguration'
    __CRAWLER_OBJ_NAME: str = 'concreteCrawler'
    __CRAWLING_RESULT_OBJ_NAME: str = 'concreteCrawlingResult'
    __EXCEPTION_OBJ_NAME: str = 'concreteException'
    __LOGGING_OBJ_NAME: str = 'concreteLogging'
    __OBJECT_FACTORY_OBJ_NAME: str = 'concreteObjectFactory'
    __LOADED_OBJECT_MSG: str = 'Object "{0}" loaded for "{1}"'
    __CONCRETE_OBJ_REQUIRED: str = 'A concrete object for "{0}" is required. This crawler cannot run'

    def __init__(self, dependecies_file_path: str, crawler_config_file_path: str):
        super().__init__()
        
        if (dependecies_file_path is None or dependecies_file_path == '') or (crawler_config_file_path is None or crawler_config_file_path == ''):
            raise Exception("Path to dependencies and configuration files is required")
            pass

        self.__dep_file_path = dependecies_file_path
        self.__crawler_config_file_path = crawler_config_file_path

        self.__object_factory = ObjectFactory()
        self.__object_factory.LoadDependencies('')

        self.__crawler = self.__object_factory.GetInstance(self.__CRAWLER_OBJ_NAME, ICrawler)
        self.__apiController = self.__object_factory.GetInstance(self.__API_CONTROLLER_OBJ_NAME, IApiController)
        self.__configuration = self.__object_factory.GetInstance(self.__CONFIGURATION_OBJ_NAME, IConfiguration)
        self.__crawlingResult = self.__object_factory.GetInstance(self.__CRAWLING_RESULT_OBJ_NAME, ICrawlingResult)
        self.__exception = self.__object_factory.GetInstance(self.__EXCEPTION_OBJ_NAME, IException)
        self.__logging = self.__object_factory.GetInstance(self.__LOGGING_OBJ_NAME, ILogging)

        self.check_concrete_object_is_none(self.__exception, "IException")
        self.check_concrete_object_is_none(self.__crawler, "ICrawler")
        self.check_concrete_object_is_none(self.__logging, "ILogging")
        self.check_concrete_object_is_none(self.__crawling_result, "ICrawlingResult")
        self.check_concrete_object_is_none(self.__configuration, "IConfiguration")
        self.check_concrete_object_is_none(self.__api_controller, "IApiController")

        self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__crawler), type(ICrawler)))
        self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__api_controller), type(IApiController)))
        self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__configuration), type(IConfiguration)))
        self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__crawling_result), type(ICrawlingResult)))
        self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__exception), type(IException)))
        self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__logging), type(ILogging)))

    def execute(self):
        try:
            self.__configuration.Load('FILE_PATH', 'SECTION_NAME')
            destination_url: str = self.__configuration.Read('FIELD_URL')
            crawling_args: dict = self.__configuration.Read('FIELD_ARGS')

            self.__logging.Log("Crawling has started")
            result: ICrawlingResult = self.__crawler.Execute(crawling_args)
            
            if result is None:
                raise Exception("Crawling result cannot be null")
                pass
            
            result_obj: dict = result.GetObject()

            if result_obj is None:
                raise Exception("Crawling result object cannot be null")
                pass

            self.__logging.Log("Sending crawling result to destination URL")
            self.__api_controller.PostAssync('URL', 'HEAD', )

            self.__logging.Log("DONE HERE! :)")
            pass
        except Exception as ex:
            
            pass
        pass

    def check_concrete_object_is_none(self, concrete_obj: object, expected_type_name: str):
        if (concrete_obj is None) and (self.__exception is None):
            raise Exception(self.__CONCRETE_OBJ_REQUIRED.format(expected_type_name))
            pass
        elif (concrete_obj is None):
            self.__exception.ManageException(self.__CONCRETE_OBJ_REQUIRED.format(expected_type_name))
            pass
        pass
    pass