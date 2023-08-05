class Error(Exception):
    """
    Attributes:
        response_content: Response content from logic monitor
        response_status: Response status code. Basically HTTP status code
        msg: Error message
    """

    def __init__(
            self,
            response_content: str,
            response_status: int,
            msg: str
    ):
        self.response_content = response_content
        self.response_status = response_status
        self.msg = msg


class InvalidItemsError(Error):
    """ Raised when the number of expected items returned from logicmonitor is not correct """
    pass


class RequestFailedError(Error):
    """ If return status code is not ok """
    pass


class ItemNotAvailable(Error):
    """ If the the item is not available on logicmonitor """
    pass
