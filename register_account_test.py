from register_account import RegisterAccounts
from unittest import mock

import unittest
import json
import requests


class MockResponse(requests.Response):
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.reason = ''
        self.url = ''

    def json(self):
        return self.json_data
    
def mocked_test_read_csv_successful(*args, **kwargs):
    if args[0] == "accounts.csv":
        return MockResponse({"success":True, "rows_total":15, "success_total":5, "failed_total":7},200)
    return MockResponse(None, 400)

def mocked_test_read_csv_fail(*args, **kwargs):
    if args[0] == "":
        return MockResponse(None, FileNotFoundError)
    
    
def mocked_test_write_csv_successful(*args, **kwargs):
    if args[0] == "accounts_new.csv":
        return MockResponse({"success":True, "rows_total":5},200)
    return MockResponse(None, 400)
    

class TestRegisterAccounts(unittest.TestCase):
    
    @mock.patch('requests.get', side_effect=mocked_test_read_csv_successful)
    def test_read_csv_success(self, mock_get):
        ra = RegisterAccounts()
        ra.read_from_csv('accounts.csv')
        self.assertNotEqual(ra.rows_total, 15)

    @mock.patch('requests.get', side_effect=mocked_test_read_csv_fail)
    def test_read_csv_file(self, mock_get):
        ra = RegisterAccounts()
        with self.assertRaises(FileNotFoundError):
            ra.read_from_csv('')
    
    @mock.patch('requests.get', side_effect=mocked_test_read_csv_successful)
    def test_write_csv_success(self, mock_get):
        ra = RegisterAccounts()
        ra.write_available_users_to_csv_file()
        self.assertIsNotNone(len(ra.get_result()))
    
    def test_read_from_csv_failed_without_filename(self):
        ra = RegisterAccounts()
        with self.assertRaises(FileNotFoundError):
            ra.read_from_csv('')

    def test_read_from_csv_successful_with_valid_filename(self):
        ra = RegisterAccounts()
        ra.read_from_csv('accounts.csv')
        self.assertNotEqual(ra.rows_total, 0)

    def test_check_valid_data_return_true_with_all_valid_data(self):
        first_name = 'first_name'
        middle_name = 'middle_name'
        last_name = 'last_name'
        phone_number = '0123456789'
        social_id = '123456789'
        row = [first_name, middle_name, last_name, phone_number, social_id]

        ra = RegisterAccounts()
        result = ra.check_valid_data(row)

        self.assertTrue(result)

    def test_check_valid_data_return_false_with_first_name_is_empty(self):
        first_name = ''
        middle_name = 'middle_name'
        last_name = 'last_name'
        phone_number = '0123456789'
        social_id = '123456789'
        row = [first_name, middle_name, last_name, phone_number, social_id]

        ra = RegisterAccounts()
        result = ra.check_valid_data(row)

        self.assertFalse(result)

    def test_check_valid_data_return_false_with_phone_number_is_not_unique(self):
        first_name = 'first_name'
        middle_name = 'middle_name'
        last_name = 'last_name'
        phone_number = '0123456789'
        social_id = '123456789'
        row = [first_name, middle_name, last_name, phone_number, social_id]

        ra = RegisterAccounts()
        ra.phone_number_list = '0123456789'
        result = ra.check_valid_data(row)

        self.assertFalse(result)

    def test_get_result_output(self):
        expected_result = {
            'totalRowsUpload': 12,
            'totalSuccess': 5,
            'totalError': 7,
            'totalAccounts': 5
        }
        ra = RegisterAccounts()
        ra.read_from_csv('accounts.csv')
        result = json.loads(ra.get_result())

        self.assertEqual(result['totalRowsUpload'], expected_result['totalRowsUpload'])
        self.assertEqual(result['totalSuccess'], expected_result['totalSuccess'])
        self.assertEqual(result['totalError'], expected_result['totalError'])
        self.assertEqual(len(result['newAccounts']), expected_result['totalAccounts'])


if __name__ == '__main__':
    unittest.main()
