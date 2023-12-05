
class MatchErrorException(Exception):
    def __init__(self, message="An Error occurred during the match!"):
        self.message = message
        super().__init__(self.message)


class GoldNotFoundException(Exception):
    def __init__(self, message='Could not find gold quantity image'):
        self.message = message
        super().__init__(self.message)


class NoMinisOnBoardException(Exception):
    def __init__(self, message='Could not find minis on board!'):
        self.message = message
        super().__init__(self.message)
