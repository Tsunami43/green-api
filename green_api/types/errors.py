class ErrorRequest(Exception):
    def __init__(self, response):
        self.message = response


class ErrorType(Exception):
    def __init__(self, data):
        self.message = "Invalid Error"
        self.data = data


class OtherMessage(Exception):
    def __init__(self, data: dict):
        self.message = "Message hasn't text"
        self.data = data


class GroupMessage(Exception):
    def __init__(self, data: dict):
        self.message = "Message in Group"
        self.data = data


class KeyNotFound(Exception):
    def __init__(self, key: str, data: dict, idMessage: str=None):
        self.message = f"In Message:{idMessage} - Not Found Key |{key}|"
        self.data = data