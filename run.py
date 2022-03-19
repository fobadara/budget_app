from mimetypes import init
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

# all_income = income.get_all_values()
# all_expenses = expenses.get_all_values()

def check_input_type(input):
    # type=''
    # try:
    if(input.isnumeric()):
      os.system('cls' if os.name == 'nt' else 'clear')
      print('Invalid input. Please enter alphabets \n')
      # return False
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
  all_income = income.get_all_values()
  table = PrettyTable()
  print('Annual income sheet')
  table.field_names=all_income[0]
  for index in range(len(all_income)):
    if(index > 0):
      table.add_row(all_income[index])
  print(table)

def get_all_expenses():
  all_expenses = expenses.get_all_values()
  table = PrettyTable()
  print('Annual expenses sheet')
  table.field_names=all_expenses[0]
  for index in range(len(all_expenses)):
    if(index > 0):
      table.add_row(all_expenses[index])
  print(table)

def update_budget_new(section, data):
  '''
  convert data_array from string to number
  Add new row to budget app
  '''
  print("Updating budget........")
  budget_data = []
  for index in range(len(data)):
    if(index != 0):
        budget_data.append(int(data[index]))
    else:
        budget_data.append(data[index])
      
  worksheet = SHEET.worksheet(section)
  print(budget_data)
  # if(position[0] == "new"):
  worksheet.append_row(budget_data)
  print(
    '''
    Row updated successfully.
    ___________________________\n
    '''
  ) 
  initialize_app()
  # else:
    # worksheet.update_cell(position[0], position[1], budget_data[1])

# def update_budget_column(section,data,row,column):
        
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
        Please enter value
        Please enter the title followed by the figures seperated by commas. For example: salary,2000, 4000 4000 \n
        To update a single column enter the title followed by the figure seperated by comma.For example: salary,2000.\n
        To leave a column blank enter number zero. For example Feeding,500,0,1000,1000.\n
        Enter "Main" to return to the main page:\n
        To end the process please enter "Exit":\n
        '''
        )
        data = data.split(",")

              
    if(data):
          row = input(
            '''
            values accepted
            __________________________________\n\n
            Enter "New" to create a new row:\n
            The row starts from the very top (the heading)
            Enter the row number for example "1" to update the first row:\n
            Enter "Main" to return to the main page:\n
            To end the process please enter "Exit":\n
            '''
            )
    
   
          if(check_entered_values(convert_to_lowercase(row)) == True):
            column = input(
            '''
            Row value accepted
            __________________________________\n\n
            Enter the column number for example "1" to update the first column:\n
            Enter "Main" to return to the main page:\n
            To end the process please enter "Exit":\n
            '''
            )
            if(data):
              update_budget_column(section, data, row, column)

          elif(check_entered_values(convert_to_lowercase(row)) == "new"):
            update_budget_new(section, data)
 
            # if(check_entered_values(convert_to_lowercase(column)) == True):
            #   data = input(
            #   '''
            #   Column value accepted
            #   __________________________________\n\n
            #   Please enter the title followed by the figures seperated by commas. For example: salary,2000, 4000 4000 \n
            #   To leave a column blank enter number zero. For example Feeding,500,0,1000,1000.\n
            #   Enter "Main" to return to the main page:\n
            #   To end the process please enter "Exit":\n
            #   '''
            #   )
              

            #   data_array = data.split(",")
            #   position = [row, column]
                

def check_entered_values(value):
  if(value == 'main'):
    initialize_app()
  elif(value == 'income'):
    get_all_income()
    return True
  elif(value == 'expenses'):
    get_all_expenses()
    return True  
  elif(value == 'all'):
    get_all_income()
    get_all_expenses()
  elif(value =='update'):
    initialize_update()
  elif(value == 'exit'):
    exit()
  # elif(value == 'income' or value == 'expenses'):
  #   return True
  elif(value == 'new'):
    return 'new'
  elif(value.isnumeric()):
    return True
  else:
    print('Invalid input. Please enter the appropriate command. \n')
 
total_income=0
total_expenses=0
highest_expenses=0              

def get_total_and_highest_expenses():
  expenses_dict={}
  all_expenses=expenses.get_all_values()
  if(len(all_expenses) > 1):
    print(all_expenses)    
    for index in range(len(all_expenses)):
      if(index > 0):
        total=0
        inner=all_expenses[index]
        for index_a in range(len(inner)):
          if(index_a > 0):
            total += int(inner[index_a])
            global total_expenses
            total_expenses += int(inner[index_a])
        expenses_dict.update({inner[0]:total})
    global highest_expenses    
    highest_expenses = max(expenses_dict, key=expenses_dict.get)
  else:
    total_expenses = "Expenses is currently empty. Enter update to add values"
get_total_and_highest_expenses()  

print(highest_expenses)
print(total_expenses)

def get_total_income():
  all_income=income.get_all_values()
  if(len(all_income) > 1):
    print(all_income)    
    for index in range(len(all_income)):
      if(index > 0):
        inner=all_income[index]
        for index_a in range(len(inner)):
          if(index_a > 0):
            global total_income
            total_income += int(inner[index_a])
  else:
    total_income = "Expense is currently empty. Enter update to add values"
get_total_income()  
print(f'total-income: {total_income}')
          
def initialize_app():
  # '''
  # Terminal is cleared if user returns to main page
  # '''
  # os.system('cls' if os.name == 'nt' else 'clear')
  initialize = True
  while initialize:
    print('Please enter "All" to display all recorded income and expenses.\n')
    print('Please enter "Income" to display all recorded income.\n')
    print('Please enter "Expenses" to display all recorded expenses.\n')
    print('Please enter "Update" to make changes to the budget.\n')
    print('To end the process please enter "Exit".\n')
  
    user_input = input('Enter your data here: ')
    'Validate input type'

    if(check_input_type(user_input) == True):
      check_entered_values(convert_to_lowercase(user_input))


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