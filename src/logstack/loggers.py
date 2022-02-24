import requests
from .serializers import LogSerializer


class Logger(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    # TODO: Convert scheme to Enum
    def __init__(self, scheme: str, url: str, port: str, log_name: str) -> None:
        # TODO: Check if this violates the singleton pattern. I should not be
        #       able to reconfigure the logger after it has been created.
        self.scheme = scheme
        self.url = url
        self.port = port
        self.log_name = log_name

    def log_to_remote(self, log: LogSerializer) -> None:
        log.data['log_name'] = self.log_name
        requests.post(
            url=f"{self.scheme}://{self.url}:{self.port}/",
            json=log.data
        )

    def log_to_file() -> None:
        raise NotImplementedError

class FlaskLogger(Logger):
    pass


class FastApiLogger(Logger):
    pass