"""rmon.common.rest
"""

class RestException(Exception):
    """Base class of the exception
    """

    def __init__(self,code,message):
        """initialization of the exception
        

        Args:
            code (int): http status code
            message (str): Error message

        """
        self.code = code
        self.message = message
        super(RestException,self).__init__()

