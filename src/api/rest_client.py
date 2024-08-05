from http.client import HTTPSConnection
from base64 import b64encode
from json import loads, dumps

class RestClient:
    def __init__(self, username, password, domain):
        self.username = username
        self.password = password
        self.domain = domain

    def request(self, path, method, data=None):
        connection = HTTPSConnection(self.domain)
        try:
            base64_bytes = b64encode(f"{self.username}:{self.password}".encode("ascii")).decode("ascii")
            headers = {'Authorization': f'Basic {base64_bytes}', 'Content-Encoding': 'gzip'}
            connection.request(method, path, headers=headers, body=data)
            response = connection.getresponse()
            return loads(response.read().decode())
        finally:
            connection.close()

    def get(self, path):
        return self.request(path, 'GET')

    def post(self, path, data):
        data_str = dumps(data) if not isinstance(data, str) else data
        return self.request(path, 'POST', data_str)