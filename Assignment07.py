# --------------------------------------------------------------------------- #
# Title: Assignment 07
# Description: Working with pickling and structured error handling
#              Program pickles/unpickles lists of expenses and their amounts
#              to a binary file
#              Error handling added when finding a file and to all user inputs
# ChangeLog (Who,When,What):
# KDoehlert,8.23.2022,Created starter file based on Module 06
# KDoehlert,8.24.2022, Updated file to include pickling and error handling
# --------------------------------------------------------------------------- #

# Imports --------------------------------------------------------------------#
import pickle

# Data ---------------------------------------------------------------------- #
file_name_str = "Expenses.dat"  # The name of the data file
row_lst = []  # A row of data that will include the expense name and amount
table_lst = []  # A list that acts as a 'table' of rows
choice_str = ''  # Captures the user option selection

# Custom Exceptions
class MenuSelectionRange(Exception):
    """  Menu Selection must be 1 - 5  """
    def __str__(self):
        return 'Menu selection must be 1 - 5'


# Processing  --------------------------------------------------------------- #
class Processor:
    """  Performs Processing tasks """

    @staticmethod
    def load_data_from_file(file_name, list_of_rows):
        """ Loads data from a binary file into a list of list rows

        :param file_name: (string) with name of file:
        :param list_of_rows: (list) you want filled with file data:
        :return: (list) of list rows
        """
        try:
            list_of_rows.clear()  # clear current data
            file = open(file_name, "rb")
            list_of_rows = pickle.load(file)
        except FileNotFoundError as e:
            print() # blank line for formatting
            print("File does not exist. There is no data to load!\n")
        return list_of_rows

    @staticmethod
    def add_data_to_list(expense_name, amount, list_of_rows):
        """ Adds data to a list of list rows

        :param expense_name: (string) with name of an expense:
        :param amount: (float) with cost of the expense:
        :param list_of_rows: (list) you want filled with file data:
        :return: (list) of list rows
        """

        row = [expense_name, amount]
        list_of_rows.append(row)
        return list_of_rows

    @staticmethod
    def remove_data_from_list(expense_name, list_of_rows):
        """ Removes data from a list of list rows

        :param expense_name: (string) with name of an expense:
        :param list_of_rows: (list) you want data removed from:
        :return: (list) of list rows
        """
        for row in list_of_rows:
            if row[0].lower() == expense_name.lower():
                del list_of_rows[list_of_rows.index(row)]
        return list_of_rows

    @staticmethod
    def pickle_data_to_file(file_name, list_of_rows):
        """ Pickles data from a list of list rows to a binary file

        :param file_name: (string) with name of file:
        :param list_of_rows: (list) you want filled with file data:
        :return: (list) of list rows
        """
        file = open(file_name, "wb")
        pickle.dump(list_of_rows,file)
        file.close()
        return list_of_rows

    @staticmethod
    def sum_expenses(list_of_rows):
        """ Calculates the sum of all expenseses

            :param list_of_rows: (list) that contains amounts you want to sum
            :return: (float) sum
        """
        sum = 0.00
        for row in list_of_rows:
            num = float(row[1])
            sum = sum + num
        return sum

# Presentation (Input/Output)  -------------------------------------------- #

class IO:
    """ Performs Input and Output tasks """

    @staticmethod
    def output_menu_tasks():
        """  Display a menu of choices to the user

        :return: nothing
        """
        print('''
        Menu of Options
        1) Add a new Expense
        2) Remove an existing Expense
        3) Save Data to File
        4) Calculate total Expenses        
        5) Exit Program
        ''')
        print()  # Add an extra line for looks

    @staticmethod
    def input_menu_choice():
        """ Gets the menu choice from a user

        :return: string
        """
        try:
            choice = str(input("Which option would you like to perform? [1 to 5] - ")).strip()
            if choice not in ['1','2','3','4','5']:
             raise MenuSelectionRange()
        except MenuSelectionRange as e:
            print() # blank line for formatting
            print(e)
        print()  # Add an extra line for looks
        return choice

    @staticmethod
    def output_current_expenses_in_list(list_of_rows):
        """ Shows the current Expenses in the list of list rows

        :param list_of_rows: (list) of rows you want to display
        :return: nothing
        """
        print("******* The current expenses are: *******")
        for row in list_of_rows:
            print('Expense: ', row[0], ' | Amount: $',format(row[1],'.2f'),sep='')
        print("*******************************************")
        print()  # Add an extra line for looks

    @staticmethod
    def input_new_expense_and_amount():
        """  Gets task and priority values to be added to the list

        :return: (string, float) with expense and amount
        """
        local_amount = None
        while local_amount == None:
            try:
                local_expense = input("Enter an Expense to add: ")
                local_amount = float(input("Enter the dollar amount of the Expense: "))
            except ValueError as e:
                print() # Add an extra line for looks
                print('Expense not added. Please enter a number [12.34] for the amount.')
                print() # Add an extra line for looks
        print()  # Add an extra line for looks
        return local_expense, local_amount


    @staticmethod
    def input_expense_to_remove():
        """  Gets the task name to be removed from the list

        :return: (string) with expense name
        """
        local_expense = input("Enter the name of the Expense you would like to remove: ")
        print() # Add an extra line for looks
        return local_expense

    @staticmethod
    def output_sum_of_expenses(sum):
        """Displays the sum of all expenses
        :param sum: (float) sum of expenses to display
        :returns: nothing
        """
        print('\nThe sum of expenses all expenses is: $',format(sum,'.2f'),sep='')
        print()

# Main Body of Script  ------------------------------------------------------ #

# Step 1 - When the program starts, Load data from Expenses.dat
table_lst = Processor.load_data_from_file(file_name=file_name_str, list_of_rows=table_lst)  # read file data

# Step 2 - Display a menu of choices to the user
while (True):
    # Step 3 Show current data
    IO.output_current_expenses_in_list(list_of_rows=table_lst)  # Show current data in the list/table
    IO.output_menu_tasks()  # Shows menu
    choice_str = IO.input_menu_choice()  # Get menu option

    # Step 4 - Process user's menu choice
    if choice_str.strip() == '1':  # Add a new Expense
        expense, amount = IO.input_new_expense_and_amount()
        table_lst = Processor.add_data_to_list(expense_name=expense, amount=amount, list_of_rows=table_lst)
        continue  # to show the menu

    elif choice_str == '2':  # Remove an existing Expense
        expense = IO.input_expense_to_remove()
        table_lst = Processor.remove_data_from_list(expense_name=expense, list_of_rows=table_lst)
        continue  # to show the menu

    elif choice_str == '3':  # Pickle Data to File
        table_lst = Processor.pickle_data_to_file(file_name=file_name_str, list_of_rows=table_lst)
        print("Data Saved!\n")
        continue  # to show the menu

    elif choice_str == '4': # Calculate sum of all expenses
        float_sum = Processor.sum_expenses(list_of_rows=table_lst)
        IO.output_sum_of_expenses(sum=float_sum)
        continue # to show the menu

    elif choice_str == '5':  # Exit Program
        print("Goodbye!")
        break  # by exiting loop
