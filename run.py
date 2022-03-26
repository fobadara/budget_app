'''
Checks os type
'''
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
    '''Checks if the user enters an alphabet or a number.
       Returns an error message if the user enters a number.
    '''
    if text.isnumeric():
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Invalid input. Please enter alphabets')
    else:
        return True


def convert_to_lowercase(value):
    """
    Convert input to lower case.
    """
    return value.lower()


HIGHEST_EXPENSES = 0

def get_total_and_highest_expenses():
    """
    Loops through the numbers in the spreadsheet,
    checks for the highest expense.
    Add all the numbers to get total expenses.
    """
    total_expenses = 0

    expenses_dict = {}
    all_expenses = expenses.get_all_values()
    if len(all_expenses) > 1:
        for index, value in enumerate(all_expenses):
            if index > 0:
                total = 0
                inner = value
                for index_a, value_a in enumerate(inner):
                    if index_a > 0:
                        total += int(value_a)
                        total_expenses += int(value_a)
                expenses_dict.update({inner[0]: total})
        global HIGHEST_EXPENSES
        HIGHEST_EXPENSES = max(expenses_dict, key=expenses_dict.get)
    else:
        total_expenses = """
        Expenses is currently empty. Enter update to add values.
        """
    print(f'Total Expenses: {total_expenses}')
    print('___________________________')
    return total_expenses


def get_total_income():
    """
    Loops through the numbers in the spreadsheet.
    Add all the numbers to get total income.
    """
    total_income = 0

    all_income = income.get_all_values()

    if len(all_income) > 1:
        for index, value in enumerate(all_income):
            if index > 0:
                inner = value
                for index_a, value_a in enumerate(inner):
                    if index_a > 0:
                        total_income += int(value_a)
    else:
        total_income = """
        Income is currently empty.Enter "Update" to add values.
        """
    print(f'Total Income: {total_income}')
    print('_____________________________')
    return total_income


def check_profit_or_loss():
    expenses = get_total_and_highest_expenses()
    income = get_total_income()
    if isinstance(income, int)  and isinstance(expenses, int) :
        if income > expenses:
          print('Your money habits look good.')
          print('Your total income is greater than your expenses. You are doing well.')
          print(f'Your total income is {income}. While your total expenses is {expenses}.')
        elif expenses > income:
          print('You seem to be spending too much.')
          print(f'Your total expenses is {expenses}. While your total income is {income}.')
        else:
          print('Your income and expense are equal.')
        print('___________________________________________')
        
        
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
        table.field_names = all_income[0]
        for index in range(len(all_income)):
            if index > 0:
                table.add_row(all_income[index])
        print(table)
        get_total_income()
    else:
        print(
          '''
            Income has been cleared.
            You need to reconstruct the sheet from it's header with "Update"
          ___________________________________\n'''
        )


def get_all_expenses():
    """
    clear the terminal, get expenses from spread sheet
    and display it in a table
    """
    all_expenses = expenses.get_all_values()
    if all_expenses:
        table = PrettyTable()
        print('Annual expenses sheet')
        table.field_names = all_expenses[0]
        for index in range(len(all_expenses)):
            if index > 0:
                table.add_row(all_expenses[index])
        print(table)
        get_total_and_highest_expenses()
    else:
        print(
          '''
          Expenses has been cleared.
          '''
        )


def update_budget_new(section, data):
    '''
    Convert data_array from string to number.
    Add new row to budget app.
    '''
    if len(data) == 5:
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
        initialize_update()
    elif len(data) > 5:
        print('Error! Values are greater than five')
        print(data)
        print('Worksheet values should be a maximum of five')
        initialize_update()
    elif len(data) < 5:
        print('Error! Values are less than five')
        print(data)
        initialize_update()


def update_budget_column(section, data, row, column):
    """
    Convert data_array from string to number.
    Add new column to budget app.
    """
    if len(data) == 2:
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
        initialize_update()  
    elif len(data) > 2:
        print('Error! Values are greater than two')
        print(data)
        print('Values should be equal two when you are editing a column')
        initialize_update()
    elif len(data) <  2:
        print('Error! value is less than two')
        print(data)
        print('Values should be equal two when you are editing a column')
        initialize_update()


def initialize_update():
    """
    TO ADD DOCSTRING COMMENT HERE
    """
    initialize = True
    while initialize:
        section = input(
          '''
          Enter "Income" to update your income:
          Enter "Expenses" to update your expenses:
          Enter "Main" to return to the main page: \n
          '''
        )
        section = convert_to_lowercase(section)
        if check_entered_values(section) is True:
            data = input(
                '''
                Enter worksheet values in the following format: \n
                Enter the title followed by the figures seperated by commas.\n
                For example: salary,2000,4000,300 \n
                To update a single column enter the title followed by the
                figure seperated by comma.\n
                For example: salary,2000.\n
                To leave a column blank when creating a new row enter number zero.
                For example Feeding,500,0,1000,1000.
                And Clothing,200,0,0,0 \n
                To end the process please enter "Exit":\n
                '''
                )
            data = data.split(",")

        if data:
            row = input(
              f'''
              Data accepted
              __________________________________\n
              Enter "New Row" to add inputed values to a new {section}
              income or expenses row:\n
              The row starts from the very top (the heading)
              Enter the row number for example "1" to update the first row:\n
              Enter "Main" to return to the main page:\n
              To end the process please enter "Exit":\n
              '''
              )

            if check_entered_values(convert_to_lowercase(row)) is True:
                column = input('''

                Row value accepted
                __________________________________\n
                Enter the column number for example "1"
                to update the first column:\n
                Enter "Main" to return to the main page:\n
                To end the process please enter "Exit":\n
                ''')
                if data:
                    update_budget_column(section, data, row, column)

            elif check_entered_values(convert_to_lowercase(row)) == "new":
                update_budget_new(section, data)


def clear_worksheet():
    """
    TO ADD DOCSTRING COMMENT HERE
    """
    verification = input(
            '''Warning! all data will be lost\n
            This cannot be undone\n
            To clear income enter  "Clear Income".\n
            To clear expenses enter "Clear Expenses"\n
            To return to main type "Main"\n
            To end the process enter exit\n
            ''')
    sHEET_HEADER = ['DESCRIPTION', 'JAN-MARCH', 'APRIL-JUNE', 'JULY-SEP', 'OCT-DEC' ]
    if convert_to_lowercase(verification) == "clear income":
        worksheet = SHEET.worksheet('income')
        worksheet.clear()
        worksheet.append_row(sHEET_HEADER)
        get_all_income()


    elif convert_to_lowercase(verification) == "clear expenses":
        worksheet = SHEET.worksheet('expenses')
        worksheet.clear()
        worksheet.append_row(sHEET_HEADER)
        get_all_expenses()


def check_entered_values(value):
    """
    TO ADD DOCSTRING COMMENT HERE
    """
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
          f'''Highest Expenses: {HIGHEST_EXPENSES}
          _____________________________________\n'''
        )
    elif value == 'status':
        check_profit_or_loss()
    elif value == 'all':
        get_all_income()
        get_all_expenses()
    elif value == 'update':
        initialize_update()
    elif value == 'clear':
        clear_worksheet()
    elif value == 'exit':
        exit()
    elif value == 'new row':
        return 'new'
    elif value.isnumeric():
        return True
    else:
        print('Invalid input. Please enter the appropriate command. \n')


def initialize_app():
    """
    Display messages to guide users on how to use the app.
    """
    initialize = True
    while initialize:
        print('Welcome to the Budget App!\n')
        print('Please enter "Update" to make changes to the budget.')
        print('Please enter "Income" to display all recorded income.')
        print('Please enter "Expenses" to display all recorded expenses.')
        print('Please enter "Highest" to get your highest expenses.')
        print('Please enter "All" to display all recorded income and expenses.')
        print('Please enter "Status" to know if you are making more money or spending more money.')
        print('Enter "clear" to clear worksheet.')
        print('To end the process please enter "Exit".')
        user_input = input('Enter your data here:')
        if check_input_type(user_input) is True:
            check_entered_values(convert_to_lowercase(user_input))


initialize_app()
