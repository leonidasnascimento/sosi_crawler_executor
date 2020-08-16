from sosi_crawler_interfaces.IApiController import IApiController
from sosi_crawler_interfaces.IConfiguration import IConfiguration
from sosi_crawler_interfaces.ICrawler import ICrawler
from sosi_crawler_interfaces.ICrawlingResult import ICrawlingResult
from sosi_crawler_interfaces.IException import IException
from sosi_crawler_interfaces.ILogging import ILogging
from sosi_crawler_interfaces.IObjectFactory import IObjectFactory
from sosi_crawler_object_factory.factory import ObjectFactory

class Executor():
    '''
        1 - Load Settings
            1.1 - Concrente Crawler
            1.2 - API
            1.3 - Error Handler
            1.4 - ...
        2 - Load the concrete Crawler
        3 - Excecute the concrete Crawler
        4 - Send result to the API
        5 - Process API response (?????)
        6 - Handle Exceptions
    '''

    ## Global variables
    __objectFactory: IObjectFactory = None
    __crawler: ICrawler = None
    __apiController: IApiController = None
    __configuration: IConfiguration = None
    __crawler: ICrawler = None
    __crawlingResult: ICrawlingResult = None
    __exception: IException = None
    __logging: ILogging = None

    ## Constant Values
    __API_CONTROLLER_OBJ_NAME: str = 'concreteApiController'
    __CONFIGURATION_OBJ_NAME: str = 'concreteConfiguration'
    __CRAWLER_OBJ_NAME: str = 'concreteCrawler'
    __CRAWLING_RESULT_OBJ_NAME: str = 'concreteCrawlingResult'
    __EXCEPTION_OBJ_NAME: str = 'concreteException'
    __LOGGING_OBJ_NAME: str = 'concreteLogging'
    __OBJECT_FACTORY_OBJ_NAME: str = 'concreteObjectFactory'
    __LOADED_OBJECT_MSG: str = 'Object "{0}" loaded for "{1}"'

    def __init__(self):
        super().__init__()
        
        self.__objectFactory = ObjectFactory
        self.__objectFactory.LoadDependencies('')

        self.__crawler = self.__objectFactory.GetInstance(self.__CRAWLER_OBJ_NAME, ICrawler)
        self.__apiController: IApiController = self.__objectFactory.GetInstance(self.__API_CONTROLLER_OBJ_NAME, IApiController)
        self.__configuration: IConfiguration = self.__objectFactory.GetInstance(self.__CONFIGURATION_OBJ_NAME, IConfiguration)
        self.__crawlingResult: ICrawlingResult = self.__objectFactory.GetInstance(self.__CRAWLING_RESULT_OBJ_NAME, ICrawlingResult)
        self.__exception: IException = self.__objectFactory.GetInstance(self.__EXCEPTION_OBJ_NAME, IException)
        self.__logging: ILogging = self.__objectFactory.GetInstance(self.__LOGGING_OBJ_NAME, ILogging)

        if (self.__logging is not None):
            self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__crawler), type(ICrawler)))
            self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__apiController), type(IApiController)))
            self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__configuration), type(IConfiguration)))
            self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__crawlingResult), type(ICrawlingResult)))
            self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__exception), type(IException)))
            self.__logging.Log(self.__LOADED_OBJECT_MSG.format(type(self.__logging), type(ILogging)))
        else:
            raise Exception('The log object was not found/instantiated. It is required for crawling execution. Please check.')
            pass
    pass