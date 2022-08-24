# Pickling and Error Handling 

## Introduction
In module 7 we learned how to use pickling to save data to and load data from a binary file. We also learned how to use structured error handling to manage errors and provide more user-friendly error messages. 
In this paper I am going to discuss how I created an Expense Tracking script that uses both pickling and error handling.

## Overview of the script
The Expense Tracking script has a similar structure to the To Do List script from module 6, but instead of managing lists of dictionaries with a Task and Priority, 
it manages lists of lists with an Expense Name and Amount. The script starts by loading data from a binary file, if one exists. The user is presented with a menu of options: 1. Add a new Expense 2. Remove an existing Expense 3. Save Data to File 4. Calculate total Expenses 5. Exit Program. 

Option 4 uses two brand new functions for processing and IO to print the sum of all expenses.  Instead of reading and writing lines of data into a plain text file, the list object is pickled and unpickled. Structured error handling is included in three functions in the script.

## Pickling data
When menu option 3 is entered, the function *Processor.pickle_data_to_file* is called. This function opens a file in binary write mode using the file name that is passed in, pickles the list object that is passed in, and stores that pickled object in a binary file. Figure 1 shows the code used to create this function.
```
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
```
**Figure 1. Function to pickle the data** 

When you open the binary file in a text editor, you can see that the content is obscured. 
In Figure 2 you can see that the Expenses ‘Groceries’ and ‘Water’ are included, but you cannot easily read any other information.

![Figure2](https://github.com/kdoehlertUW/IntroToProg-Python-Mod07/blob/main/docs/Figure2.png "Figure 2")

**Figure 2. Pickled data opened in text editor**

## Error handling
Structured error handling was added in two functions where user input was collected using try-except blocks. 
The first IO function with error handling is *input_menu_choice*. For this function I created a custom exception class called MenuSelectionRange. This class returns the message ‘Menu selection must be 1-5’ when printed. Figure 3 shows the code used to create this class. 
```
class MenuSelectionRange(Exception):
    """  Menu Selection must be 1 - 5  """
    def __str__(self):
        return 'Menu selection must be 1 - 5'
```
**Figure 3. Class for custom exception used if menu selection is out of range**

The MenuSelectionRange error is raised if the user input is not 1, 2, 3, 4, or 5. When this error is raised, the error message is printed. 
The invalid selection is returned and no if statements are triggered, so the script returns to the beginning of the while loop where *IO.input_menu_choice* 
is called again, and another menu selection can be inputted. Figure 4 shows the code for this function.
```
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
```
**Figure 4. Function to get user input for menu selection**

Figure 5 shows how this error looks when the script is run in Command Prompt. An incorrect value (8) is entered, the error message is printed, 
and the script returns to the beginning of the loop where it prints the expenses and menu options. 

![Figure5](/docs/Figure5.png "Figure 5")

**Figure 5. Error handling when an incorrect menu selection [8] is made**

A try-catch block was also added to the IO function *input_new_expense_and_amount*. The input for amount is converted to a floating-point value, and anything 
other than a number is entered a ValueError is raised. The catch block prints a custom error message informing the user that the expense and amount was not 
added, and that the amount must be a number. The try-catch block is wrapped in a while loop that continues until a number is assigned to the *local_amount* variable. 
Figure 6 shows the code for this function.
```
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
```
**Figure 6. Function that gets user input for expense name and amount**

Figure 7 shows what this error handling looks like in the Command Prompt. A string (Too high) is entered as the amount, which raised the ValueError when 
trying to convert it to float. The custom error message is printed, and the user has another opportunity to enter the Expense Name and Amount until a valid
entry is made.

![Figure7](/docs/Figure7.png "Figure 7")

**Figure 7. Error handling when an incorrect value [Too high] is entered for amount**

## Unpickling and error handling
The Processor function *load_data_from_file* combines unpickling and structured error handling. The code to load the pickled list and assign it to *list_of_rows* is
wrapped in a try-except block. This is necessary because the file is being opened in “rb” mode and will raise an error if the file does not exist. 
With the try-catch block added, an error message with be printed if the file does not exist, but the script will continue. Figure 8 shows the code using both
unpickling and error handling.
```
def load_data_from_file(file_name, list_of_rows):
    """ 
    Loads data from a binary file into a list of list rows
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
```
**Figure 8. Function to unpickle the data wrapped in a try-except block**

Figure 9 shows the error message that is printed when the script is run but the binary file does not exist.

![Figure9](/docs/Figure9.png "Figure 9")

**Figure 9. Error message that is generated if there is no binary file to load from**

## Summary
In this paper I discussed how I created a script that stores a list of data related to expenses by pickling it to the binary file. 
The script also used try-except blocks to handle common errors that could occur when running the application.  
