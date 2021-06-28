import unittest
import json
import requests
from unittest import mock
from account import AccountRegister, CSV_FILE, Account




class TestAccountRegister(unittest.TestCase):
    def test_read_from_csv_failed_without_filename(self):
        account_register = AccountRegister()
        with self.assertRaises(FileNotFoundError):
            account_register.read_from_csv('')

    def test_read_from_csv_successful_with_valid_filename(self):
        account_register = AccountRegister()
        account_register.read_from_csv(CSV_FILE)
        self.assertNotEqual(len(account_register.accounts), 0)

    def test_get_duplicate_dictionary(self):
        expected_result = {
            
            'totalAccounts': 2
        }
        account_register = AccountRegister()
        account_register.read_from_csv(CSV_FILE)
        result = account_register.get_duplicate_row()
        self.assertEqual(len(result), expected_result['totalAccounts'])

    def test_get_valid_dictionary(self):
        expected_result = {
            
            'totalAccounts': 8
        }
        account_register = AccountRegister()
        account_register.read_from_csv(CSV_FILE)
        result = account_register.get_valid_row()
        self.assertEqual(len(result), expected_result['totalAccounts'])
        
        
    


if __name__ == '__main__':
    unittest.main()
