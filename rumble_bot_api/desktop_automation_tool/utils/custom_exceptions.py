class WindowNotFoundException(Exception):
    def __init__(self, message='window can not be found!'):
        self.message = message
        super().__init__(self.message)


class ElementNotFoundException(Exception):
    def __init__(self, message="Element Not Found!"):
        self.message = message
        super().__init__(self.message)
