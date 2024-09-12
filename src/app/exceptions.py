class InvalidCustomerIdException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidPageException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class CustomerNotFoundException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)