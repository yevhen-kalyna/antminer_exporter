class KernelLogError(Exception):
    """Exception raised for errors in the Kernel Logs.

    Attributes:
        log_row -- input log row which caused the error
        message -- explanation of the error
    """

    def __init__(self, log_row, message):
        self.log_row = log_row
        self.message = message
        super().__init__(self.message)