import os
import gspread
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('budget_app')

income = SHEET.worksheet('income')
expenses = SHEET.worksheet('expenses')

def check_input_type(text):
    if text.isnumeric():
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Invalid input. Please enter alphabets \n')
    else:
        return True

def convert_to_lowercase(value):
    return value.lower()

highest_expenses=0

def get_total_and_highest_expenses():
    total_expenses=0

    expenses_dict={}
    all_expenses=expenses.get_all_values()
    if len(all_expenses) > 1:
        for index in range(len(all_expenses)):
            if index > 0:
                total=0
                inner=all_expenses[index]
                for index_a in range(len(inner)):
                    if index_a > 0:
                        total += int(inner[index_a])
                        total_expenses += int(inner[index_a])
                expenses_dict.update({inner[0]:total})
        global highest_expenses  
        highest_expenses = max(expenses_dict, key=expenses_dict.get)
    else:
        total_expenses = "Expenses is currently empty. Enter update to add values"
    print(f'Total Expenses: {total_expenses}\n')

def get_total_income():
    total_income=0

    all_income=income.get_all_values()
    if len(all_income) > 1:
        for index in range(len(all_income)):
            if index > 0:
                inner=all_income[index]
                for index_a in range(len(inner)):
                    if index_a > 0:
                        total_income += int(inner[index_a])
    else:
        total_income = 'Income is currently empty. Enter "Update" to add values.\n'
    print(f'Total Income: {total_income}\n')

def get_all_income():
    """
    clear the terminal, get income from spread sheet
    and display it in a table
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    all_income = income.get_all_values()
    if all_income:
        table = PrettyTable()
        print('Annual Income Sheet')
        table.field_names=all_income[0]
        for index in range(len(all_income)):
            if index > 0:
                table.add_row(all_income[index])
        print(table)
        get_total_income()
    else:
        print(
          '''
            Income has been cleared. You need to reconstruct the sheet from its header with "Update"
          ___________________________________\n'''
        )

def get_all_expenses():
    all_expenses = expenses.get_all_values()
    if all_expenses:
        table = PrettyTable()
        print('Annual expenses sheet')
        table.field_names=all_expenses[0]
        for index in range(len(all_expenses)):
            if index > 0:
                table.add_row(all_expenses[index])
        print(table)
        get_total_and_highest_expenses()
    else:
        print(
          '''
          Expenses has been cleared. You need to reconstruct the sheet from its header with "Update"
          ___________________________________\n
          '''
        )

def update_budget_new(section, data):
    '''
    convert data_array from string to number
    Add new row to budget app
    '''
    print("Updating budget........")
    budget_data = []
    for index in range(len(data)):
        if index != 0:
            budget_data.append(int(data[index]))
        else:
            budget_data.append(data[index])
        
    worksheet = SHEET.worksheet(section)
    print(budget_data)
    worksheet.append_row(budget_data)
    print(
      '''
      Row updated successfully.
      ___________________________\n
      '''
    ) 
    initialize_app()
        
def update_budget_column(section, data, row, column):
    print("Updating budget........")
    print(data)
    worksheet = SHEET.worksheet(section)
    worksheet.update_cell(row, column, data[1])
    print(
      '''
      Column updated successfully.
      ___________________________\n
      '''
    )
    initialize_app()
 
def initialize_update():
    initialize = True
    while initialize:
        section = input(
          '''
          Enter "Income" to update your income:\n
          Enter "Expenses" to update your expenses:\n
          '''
        )
        if(check_entered_values(convert_to_lowercase(section)) == True):
            data = input(
            '''
            Enter worksheet values in the following format: \n
            Enter the title followed by the figures seperated by commas.\n 
            For example: salary,2000,4000,300 \n
            To update a single column enter the title followed by the figure seperated by comma.\n
            For example: salary,2000.\n
            To leave a column blank enter number zero. For example Feeding,500,0,1000,1000.\n
            Enter "Main" to return to the main page:\n
            To end the process please enter "Exit":\n
            '''
            )
            data = data.split(",")

        
        if data:
            row = input(
              '''
              Data accepted
              __________________________________\n\n
              Enter "New" to create a new row:\n
              The row starts from the very top (the heading)
              Enter the row number for example "1" to update the first row:\n
              Enter "Main" to return to the main page:\n
              To end the process please enter "Exit":\n
              '''
              )

            if check_entered_values(convert_to_lowercase(row)) == True:
                column = input(
                '''
                Row value accepted
                __________________________________\n\n
                Enter the column number for example "1" to update the first column:\n
                Enter "Main" to return to the main page:\n
                To end the process please enter "Exit":\n
                '''
                )
                if data:
                    update_budget_column(section, data, row, column)

            elif check_entered_values(convert_to_lowercase(row)) == "new":
                update_budget_new(section, data)

def clear_worksheet():
    verification = input(
      '''
      Warning! all data including worksheet header will be lost\n
      This cannot be undone\n
      You will need to reconstruct the sheet starting from its header for future usage with "update"\n
      To clear income enter  "Clear Income". To clear expenses enter "Clear Expenses"\n
      To return to main type "Main"
      To end the process enter exit\n
      '''
    )
    if convert_to_lowercase(verification) == "clear income":
        SHEET.worksheet('income').clear()
        get_all_income()
    elif convert_to_lowercase(verification) == "clear expenses":
        SHEET.worksheet('expenses').clear()
        get_all_expenses()                

def check_entered_values(value):
    if value == 'main':
        initialize_app()
    elif value == 'income':
        get_all_income()
        return True
    elif value == 'expenses':
        get_all_expenses()
        return True
    elif value == 'highest':
        get_total_and_highest_expenses()
        print(
          f'''Highest Expenses: {highest_expenses}
          _____________________________________\n'''
        )  
    elif value == 'all':
        get_all_income()
        get_all_expenses()
    elif value =='update':
        initialize_update()
    elif value == 'clear':
        clear_worksheet()
    elif value == 'exit':
        exit()
    elif value == 'new':
        return 'new'
    elif value.isnumeric():
        return True
    else:
        print('Invalid input. Please enter the appropriate command. \n')
 
          
def initialize_app():
    initialize = True
    while initialize:
        print('Please enter "All" to display all recorded income and expenses.\n')
        print('Please enter "Income" to display all recorded income.\n')
        print('Please enter "Expenses" to display all recorded expenses.\n')
        print('Please enter "Update" to make changes to the budget.\n')
        print('Please enter "Highest" to get the your highest expenses.\n')
        print('Enter "clear" to clear worksheet.\n')
        print('To end the process please enter "Exit".\n')
      
        user_input = input('Enter your data here: ')
        'Validate input type'

        if check_input_type(user_input) == True:
            check_entered_values(convert_to_lowercase(user_input))


initialize_app()
