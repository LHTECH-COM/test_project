import csv
import json 
import datetime
CSV_FILE = "account_03.csv"
NEW_CSV_FILE = "account_03_new.csv"

ID_INDEX = 0
FIRST_NAME_INDEX = 1
LAST_NAME_INDEX = 2
DOB_INDEX = 3

class Account():
    """
    A class to represent a user.

    Attributes
    ----------
    id: str
        id of the person
    first_name : str
        first name of the person
    last_name : str
        last name of the person
    dob : str
        date of birth of the person
    
    
    Methods
    -------
    format_dob():
        format date of birth
    
    """
    def __init__(self, info):
        self.id = info["id"]
        self.first_name = info["first_name"]
        self.last_name = info["last_name"]
        self.dob = info["dob"]
    
    #format data of birth with m/d/Y
    def format_dob(self):
        try:
            dob = datetime.datetime.strptime(self.dob,'%d%m%Y').date()
        except Exception as ex:
            print ("Invalid DOB")
            dob = self.dob
        return f'{dob}'
        
"""
    A class to register accounts for users from csv file.

    Attributes
    ----------
    accounts : object
        list of user
        
    Methods
    -------
    read_from_csv(): void
        Read all data from csv file.
    get_duplicate_row(): void
        Returns result as json format.
    get_valid_row(): void
        Returns result as json format.
    write_available_users_to_csv_file(): void
        Write all valid accounts to new file.
    
    """
class AccountRegister():
    def __init__(self):
        self.accounts = []
    
    #count num of row have the same id
    def count_id(self,id):
        data = list(filter(lambda x: x.id == id, self.accounts))
        return len(data)
        
    #read data from csv file
    def read_from_csv(self, file_name):
        try:
            with open(file_name, "r") as file:
                reader = csv.reader(file, delimiter=",")
                for index, line in enumerate(reader):
                    if index == 0:
                        continue
                    else:
                        
                        user_info = {
                            "id":line[ID_INDEX],
                            'first_name': line[FIRST_NAME_INDEX],
                            'last_name': line[LAST_NAME_INDEX],
                            'dob': line[DOB_INDEX],
                        }
                        self.accounts.append(Account(user_info))
            
            print('Read accounts from csv file successfully.')
        except FileNotFoundError:
            raise
            print('Read accounts from csv file failed.')
            
    
    #get row have duplicate id
    def get_duplicate_row(self):
        data = filter(lambda x: self.count_id(x.id) > 1, self.accounts)
        return [json.dumps({
                'id':account.id,
               'first_name': account.first_name,
                'last_name': account.last_name,
                'dob': account.dob
            }) for account in data]
        
    #return list of valid data 
    def get_valid_row(self):
        data = filter(lambda x: self.count_id(x.id) == 1, self.accounts)
        return [json.dumps({
                'id':account.id,
               'first_name': account.first_name,
                'last_name': account.last_name,
                'dob': account.format_dob()
            }) for account in data]
        
    #write data to csv file
    def write_available_users_to_csv_file(self):
        data = filter(lambda x: self.count_id(x.id) == 1, self.accounts)
        try:
            with open(NEW_CSV_FILE, mode='w') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
 
                writer.writerow(['ID', 'First Name', 'Last Name', 'DOB'])
 
                for account in data:
                    writer.writerow([account.id,account.first_name, account.last_name, account.format_dob()])
                print ("write to csv file successfully")
        except FileNotFoundError as err:
            raise
            print(err)
    
    
        
            
if __name__ == "__main__":
    
    account_register = AccountRegister()
    account_register.read_from_csv(CSV_FILE)
    print ("list duplicate row data:")
    print (account_register.get_duplicate_row())
    print ("list valid row data:")
    print (account_register.get_valid_row())

    print("Write processed data to new CSV file:")
    account_register.write_available_users_to_csv_file()            
