from sosi_crawler_interfaces import (IApiController, IConfiguration, ICrawler, ICrawlingResult, IException, ILogging, IObjectFactory)
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

    def __init__(self):
        super().__init__()
        
        ## Load Dependencies
        self.__obj_factory: IObjectFactory = ObjectFactory()
        self.__obj_factory.LoadDependencies("")

        if (__obj_factory is not None):
            self.__crawler: ICrawler = self.__obj_factory.GetInstance("", ICrawler)
    pass