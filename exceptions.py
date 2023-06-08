class LoginRequired(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class VideoUnavailable(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class VideoAgeRestricted(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class VideoPrivate(Exception):
    def __init__(self, message: str):
        super().__init__(message)