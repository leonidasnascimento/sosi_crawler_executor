from sosi_crawler_interfaces.IException import IException

class LogException(IException):
    """
    Generic Exception Class
    """
    def __init__(self):
        super().__init__()

    def manage_exception(self, ex: Exception, raise_exception: bool) -> str:
        raise AttributeError(str(ex))