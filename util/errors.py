import requests
import wrapt

class MyException(Exception):
    def __init__(self, code, message):
        self._code = code
        self._message = code


class AuthException(MyException): pass


class OtherException(MyException): pass


@wrapt.decorator
def requests_exceptions_handler(wrapped, instance, args, kwargs): # CORRECT
    def handle_exceptions():
        try:
            wrapped(*args, **kwargs)
        except requests.exceptions.HTTPError as httpErr:
            print("Http Error:", httpErr)
        except requests.exceptions.ConnectionError as connErr:
            print("Error Connecting:", connErr)
        except requests.exceptions.Timeout as timeOutErr:
            print("Timeout Error:", timeOutErr)
        except requests.exceptions.RequestException as reqErr:
            print("Something Else:", reqErr)

    return handle_exceptions()
