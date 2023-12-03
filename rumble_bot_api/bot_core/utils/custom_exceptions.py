
class ElementNotFoundException(Exception):
    def __init__(self, message="Element Not Found!"):
        self.message = message
        super().__init__(self.message)


class ImageNotFoundException(Exception):
    def __init__(self, message="Image Not Found!"):
        self.message = message
        super().__init__(self.message)


class MatchErrorException(Exception):
    def __init__(self, message="An Error occurred during the match!"):
        self.message = message
        super().__init__(self.message)


class GoldNotFoundException(Exception):
    def __init__(self, message='Could not find gold quantity image'):
        self.message = message
        super().__init__(self.message)
