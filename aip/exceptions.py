from requests import Response


class APIException(Exception):
    def __init__(self, response: Response):
        error_data = response.json()
        self.status_code = response.status_code
        self.error_code = error_data.get("error_code")
        self.message = error_data.get("message")

    def __str__(self):
        message = f"[{self.status_code}]{self.error_code}:{self.message}"
        return message
