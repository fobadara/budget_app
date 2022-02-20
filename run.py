from turtle import clear
from click import prompt
import gspread
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable
import os

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

all_income = income.get_all_values()
all_expenses = expenses.get_all_values()

def check_input_type(input):
    # type=''
    # try:
    if(input.isnumeric()):
      os.system('cls' if os.name == 'nt' else 'clear')
      print('Invalid input. Please enter alphabets \n')
      return False
    else:
      return True

    # Convert it into integer
    #     val = int(input)
    #     raise ValueError(
    #       f'Expected alphabets. You entered a number'
    #     )
    # except ValueError:
    #     try:
    #         # Convert it into float
    #         val = float(input)
    #         raise ValueError(
    #           f'Expected alphabets. You entered a number'
    #         )
    #     except ValueError as e:
    #         print(f'Invalid data {e}. Please try again. \n')
    #         return False

def convert_to_lowercase(value):
  return value.lower()

def get_all_income():
  """
  clear the terminal, get income from spread sheet
  and display it in a table
  """
  os.system('cls' if os.name == 'nt' else 'clear')
  table = PrettyTable()
  print('Annual income sheet')
  table.field_names=all_income[0]
  table.add_row(all_income[1])
  print(table)

def get_all_expenses():
  table = PrettyTable()
  print('Annual expenses sheet')
  table.field_names=all_expenses[0]
  table.add_row(all_expenses[1])
  print(table)

def check_entered_values(value):
  if(value == 'income'):
    get_all_income()
  elif(value == 'expenses'):
    get_all_expenses()  
  elif(value == 'all'):
    get_all_income()
    get_all_expenses()
  elif(value == 'exit'):
    exit()
  else: 
    print('Invalid input. Please enter the appropriate command. \n')
# get_all_income()  


# get_all_expenses()

def initialize_app():
  test= True
  while test:
    print('Please enter "All" to display all recorded income and expenses.')
    print('Please enter "Income" to display all recorded income.')
    print('Please enter "Expenses" to display all recorded expenses.')
    print('To end the process please enter "Exit".')
  
    user_input = input('Enter your data here: ')
    # Validate input type
    if(check_input_type(user_input) == False):
      continue
    else:
      check_entered_values(convert_to_lowercase(user_input))
      
    # if(type == 'alphabet'):
        # convert_to_lowercase
    # test = False

initialize_app()
# test= True

# while test:
#   """Get year and convert to string"""
#   YEAR = int(input("Please enter a budget year between 2020 and 2030:\n"))
#   if YEAR > 2030 or YEAR < 2020:
#       input("Invalid entry.Please enter a budget year between 2020 and 2030:\n")
#   else:
#     print("Valid input")
  
#   MONTH = input("Month please")
  
#   """
#   And you continue the rest like that 
#   once you are done return FALSE and it should be in a function
#   after false outside while loop you add each variable into spread sheet
#   """
#   test = False
# print(YEAR)