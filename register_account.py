from utils import *
import json
import csv
from datetime import date

CSV_FILE = "accounts.csv"
NEW_CSV_FILE = "accounts_new.csv"

FIRST_NAME_INDEX = 0
MIDDLE_NAME_INDEX = 1
LAST_NAME_INDEX = 2
PHONE_NUMBER_INDEX = 3
SOCIAL_ID_INDEX = 4

SHORT_DATE_FORMAT = '%d%m%y'


class User:
    """
    A class to represent a user.

    Attributes
    ----------
    first_name : str
        first name of the person
    last_name : str
        last name of the person
    middle_name : str
        middle name of the person
    phone_number: str
        phone number of the person
    social_id: str
        social id of the person
    created_date: date
        the date the person is created
    account_number: str
        unique account number created for the person

    Methods
    -------
    get_full_name():
        Prints the full name of the person.
    get_account_number():
        Returns account number of the person.
    """

    def __init__(self, info):
        self.first_name = info['first_name']
        self.last_name = info['last_name']
        self.middle_name = info['middle_name']
        self.phone_number = info['phone_number']
        self.social_id = info['social_id']
        self.created_date = info['created_date']
        self.account_number = ""

    def get_full_name(self):
        """Construct full name of the person"""
        return f'{self.first_name} {self.middle_name} {self.last_name}'

    def get_account_number(self):
        """Create a new account number for the person if it is not existing, otherwise just returns created one"""
        if not self.account_number:
            random_number_8_digits = random_with_N_digits(8)
            created_day = self.created_date.strftime(SHORT_DATE_FORMAT)

            self.account_number = f'IB{created_day}{random_number_8_digits}'

        return self.account_number

class RegisterAccounts:
    """
    A class to register accounts for users from csv file.

    Attributes
    ----------
    rows_total : int
        total number of rows read from the csv file.
    success_total : int
        total number of rows read successfully (all data of a row is valid) from the csv file.
    failed_total : int
        total number of rows read unsuccessfully (some data of a row is invalid) from the csv file.
    accounts: array of str
        list of accounts
    
    Methods
    -------
    check_valid_data(): bool
        Check each row data whether all essential data is valid or not.
    read_from_csv(): void
        Read all data from csv file.
    get_result(): object
        Returns result as json format.
    write_available_users_to_csv_file(): void
        Write all valid accounts to new file.
    """
    social_id_list = []
    phone_number_list = []
    
    def __init__(self):
        self.rows_total = 0
        self.success_total = 0
        self.failed_total = 0
        self.accounts = []
            
    #check valid data read from csv file
    def check_valid_data(self, row_data):
        first_name = row_data[FIRST_NAME_INDEX]
        last_name = row_data[LAST_NAME_INDEX]
        phone = row_data[PHONE_NUMBER_INDEX]
        social_id = row_data[SOCIAL_ID_INDEX]
        
        is_first_name_valid = bool(first_name.strip()) and not first_name.isnumeric()
        is_last_name_valid = bool(last_name.strip()) and not last_name.isnumeric()
        is_phone_number_valid = len(phone) == 10 and phone.isnumeric() and phone not in self.phone_number_list
        is_social_id_valid = len(social_id) == 9 and social_id.isnumeric() and social_id not in self.social_id_list
        
        return is_first_name_valid and is_last_name_valid and is_phone_number_valid and is_social_id_valid
    
    #read data from csv file
    def read_from_csv(self, file_name):
        try:
            with open(file_name, "r") as file:
                reader = csv.reader(file, delimiter=",")
                for index, line in enumerate(reader):
                    if index == 0:
                        continue
                    else:
                        if self.check_valid_data(line):
                            self.phone_number_list.append(line[PHONE_NUMBER_INDEX])
                            self.social_id_list.append(line[SOCIAL_ID_INDEX])
                            user_info = {
                                'first_name': line[FIRST_NAME_INDEX],
                                'middle_name': line[MIDDLE_NAME_INDEX],
                                'last_name': line[LAST_NAME_INDEX],
                                'phone_number': line[PHONE_NUMBER_INDEX],
                                'social_id': line[SOCIAL_ID_INDEX],
                                'created_date': date.today()
                            }
                            self.accounts.append(User(user_info))
                            self.success_total +=1
                        else:
                            self.failed_total +=1
                    self.rows_total +=1
            
            print('Read accounts from csv file successfully.')
        except FileNotFoundError:
            
            print('Read accounts from csv file failed.')
            raise
            
               
    #get list of data read from csv file
    def get_result(self):
        return json.dumps({
            'totalRowsUpload': self.rows_total,
            'totalSuccess': self.success_total,
            'totalError': self.failed_total,
            'newAccounts': [json.dumps({
                'fullName': account.get_full_name(),
                'phone_number': account.phone_number,
                'social_id': account.social_id,
                'account_number': account.get_account_number()
            }) for account in self.accounts]
        })
    
    #write data to csv file
    def write_available_users_to_csv_file(self):
        try:
            with open(NEW_CSV_FILE, mode='w') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')

                writer.writerow(['Full name', 'Phone number', 'Social ID', 'Account number'])

                for account in self.accounts:
                    writer.writerow([account.get_full_name(), account.phone_number, account.social_id, account.get_account_number()])
            print ("Write data to csv file successfully")
        except OSError as err:
            print(err)
    
    
    
if __name__ == "__main__":
    
    ra = RegisterAccounts()
    #read data from csv file
    ra.read_from_csv(CSV_FILE)
    #get list all data read from csv file
    print(ra.get_result())
    #write data to csv file
    ra.write_available_users_to_csv_file()
    
    
