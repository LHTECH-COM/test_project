from data import Account, API_URL
from unittest import mock
import json
import unittest
import requests

class MockResponse(requests.Response):
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.reason = ""
        self.url = ""

    def json(self):
        return self.json_data


def mocked_get_api_uuid_successful(*args, **kwargs):
    if args[0] == API_URL:
        return MockResponse({"success":True, "uuid":"d60dfd5e-ec46-4584-96cb-ee6c45166dd8"},200)
    return MockResponse(None, 400)

def mocked_get_api_uuid_fail(*args, **kwargs):
    if args[0] == API_URL:
        return MockResponse(None, 500)
    
class TestAccount(unittest.TestCase):
    @mock.patch('requests.get', side_effect=mocked_get_api_uuid_successful)
    def test_get_uuid_success(self, mock_get):
        row = {
            "first_name":"first_name",
            "last_name":"last_name",
            "ip_address":"ip_address",
            }
        ac = Account(row)
        result = ac.get_uuid()
        self.assertIsNotNone(result)
        
    @mock.patch('requests.get', side_effect=mocked_get_api_uuid_fail)
    def test_get_uuid_fail(self, mock_get):
        row = {
            "first_name":"first_name",
            "last_name":"last_name",
            "ip_address":"ip_address",
            }
        ac = Account(row)
        with self.assertRaises(requests.exceptions.HTTPError):
            ac.get_uuid()


if __name__ == "__main__":
    unittest.main()        
        
        
        
        
        
        
        