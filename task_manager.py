# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files. Alternatively,
# you can change directory as in the code just below.

#=====importing libraries===========
import os
from datetime import datetime, date

# Change directory if you wish!
# os.chdir("C:\\Users\\zanua\\Desktop\\Zain\\HyperionDev\\Software_Engineering_(Fundamentals)\\T17")
# print()
# print(os.getcwd())

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass


# task data in nested lists
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

    # Task lists in list
    task_data_lists = []
    for i in task_data:
        task_data_list = i.split(";")
        task_data_lists.append(task_data_list)

# Task dictionaries in list
task_data_dicts = []
for task_string in task_data:
    current_task = {}

    # Split by semicolon and manually add each component
    task_components = task_string.split(";")
    current_task['username'] = task_components[0]
    current_task['title'] = task_components[1]
    current_task['description'] = task_components[2]
    current_task['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    current_task['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    current_task['completed'] = True if task_components[5] == "Yes" else False

    task_data_dicts.append(current_task)

task_number_list = [task_data_lists.index(task_data_lists[i]) for i in range(len(task_data_lists))]



#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Dictionary with username:password pairs
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

# Creates a list of users which is used later on
users = list(username_password.keys())

# The program starts here, prompting the user to log in.
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

#========Creating Functions=========



def reg_user():
    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    new_username = input("New Username: ")
    
    # - ensures new_username is not the same as an existing username
    usernames = []
    with open("user.txt", "r") as users_file:
        for line in users_file:
            # print(line)
            username_and_password = line.split(";")
            # print(username_and_password)
            # print(username_and_password[0])
            usernames.append(username_and_password[0])

        # print(usernames)

        while new_username in usernames:
            new_username = input("That username already exists. Please enter another: ")

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("\nNew user added!")
        username_password[new_username] = new_password
            
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")
    pass

def add_task():
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
         - A username of the person whom the task is assigned to,
         - A title of a task,
         - A description of the task and 
         - the due date of the task.'''
    
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return True
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_data_dicts.append(new_task)
    with open("tasks.txt", "w") as task_file:
        tasks_list_to_write = []
        for t in task_data_dicts:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            tasks_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(tasks_list_to_write))
    print("Task successfully added.")

def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
       format of Output 2 presented in the task pdf (i.e. includes spacing
       and labelling) 
    '''

    print("\n----------------All Tasks----------------\n")

    try:
        for task_dictionary in task_data_dicts:
            
            task_number = task_data_dicts.index(task_dictionary)
            task_dictionary['completed'] = True if task_data_lists[task_number][5] == "Yes" else False

            display_string =  ("%-20s %s" %("Task Number: ",   f"{task_number}\n"))
            display_string += ("%-20s %s" %("Title: ",         f"{task_dictionary['title']}\n"))
            display_string += ("%-20s %s" %("Assigned to: ",   f"{task_dictionary['username']}\n"))
            display_string += ("%-20s %s" %("Date Assigned: ", f"{task_dictionary['assigned_date'].date()}\n"))
            display_string += ("%-20s %s" %("Due Date: ",      f"{task_dictionary['due_date'].date()}\n"))
            display_string += ("%-20s %s" %("Description: ",   f"{task_dictionary['description']}\n"))
            display_string += ("%-20s %s" %("Completed: ",     f"{task_dictionary['completed']}\n"))
            print(display_string)
        
        print("--------------------------")
    except IndexError:
        print("""Please exit the program and run again for the most
recently added task(s) to be included!""")
        print()
        print("--------------------------")


def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
       format of Output 2 presented in the task pdf (i.e. includes spacing
       and labelling)
    '''

    print("\n---------------Your Tasks----------------\n")

    # empty list for task_numbers associated with the
    # current user's tasks
    my_task_numbers = []

    # empty dictionary for number, task pairs
    # helpful for displaying specific tasks later on
    numbered_dictionary = {}

    try:

        # The for loop dislays all the tasks related to a
        # specific user.
        for task_dictionary in task_data_dicts:
            if task_dictionary['username'] == curr_user:

                task_number = task_data_dicts.index(task_dictionary)
                numbered_dictionary[task_number] = task_data_dicts[task_number]
                task_dictionary['completed'] = True if task_data_lists[task_number][5] == "Yes" else False

                my_task_numbers.append(task_number)

                display_string =  ("%-20s %s" %("Task Number: ",   f"{task_number}\n"))
                display_string += ("%-20s %s" %("Title: ",         f"{task_dictionary['title']}\n"))
                display_string += ("%-20s %s" %("Assigned to: ",   f"{task_dictionary['username']}\n"))
                display_string += ("%-20s %s" %("Date Assigned: ", f"{task_dictionary['assigned_date'].date()}\n"))
                display_string += ("%-20s %s" %("Due Date: ",      f"{task_dictionary['due_date'].date()}\n"))
                display_string += ("%-20s %s" %("Description: ",   f"{task_dictionary['description']}\n"))
                display_string += ("%-20s %s" %("Completed: ",     f"{task_dictionary['completed']}\n"))
                print(display_string)

        print("--------------------------")
    except IndexError:
        print("""Please exit the program and run again for the most
recently added task(s) to be included!""")
        print()
        print("--------------------------")

    # Preparation for displaying a specific task

    my_task_numbers.append(-1)

    acceptable_task_choice = [str(i) for i in my_task_numbers]

    print()

    task_choice = input("""To see a specific task, type the corresponding
task number and press enter. Otherwise,
type -1 and enter: """)
    
    while task_choice not in acceptable_task_choice:
        task_choice = input("""\nInvalide task_choice. Please enter a number corresponding
to your task or the number -1: """)


    print("\n----------------Specific Task-----------------\n")

    # If the user has not selected to go back, the specific task selected is displayed.
    if task_choice != "-1":
        chosen_task_dictionary = numbered_dictionary[int(task_choice)]
        # print(chosen_task_dictionary)
    
        display_string =  ("%-20s %s" %("Task Number: ",   f"{int(task_choice)}\n"))
        display_string += ("%-20s %s" %("Title: ",         f"{chosen_task_dictionary['title']}\n"))
        display_string += ("%-20s %s" %("Assigned to: ",   f"{chosen_task_dictionary['username']}\n"))
        display_string += ("%-20s %s" %("Date Assigned: ", f"{chosen_task_dictionary['assigned_date'].date()}\n"))
        display_string += ("%-20s %s" %("Due Date: ",      f"{chosen_task_dictionary['due_date'].date()}\n"))
        display_string += ("%-20s %s" %("Description: ",   f"{chosen_task_dictionary['description']}\n"))
        display_string += ("%-20s %s" %("Completed: ",     f"{chosen_task_dictionary['completed']}\n"))
        print(display_string)

        print("--------------------------")

        # Specific Task menu

        # Once the user selects a specific task, the user is given
        # the following three options:
        mark_edit_choice = input(f"""To choose from the options below, please
type the corresponding letter and press enter:

m - mark task {task_choice} as complete
e - edit task {task_choice}
b - back to main menu

Choice: """)

        # A little defensive programming. Ensures mark_edit_choice is correct.
        while mark_edit_choice not in ["m", "e", "b"]:
            mark_edit_choice = input(f"""Invalid choice. Please type the
corresponding letter and press enter:

m - mark task {task_choice} as complete
e - edit task {task_choice}
b - back to main menu

Choice: """)

        if mark_edit_choice == "m":
            task_data_lists[int(task_choice)][5] = "Yes"

            # The whole file is re-written to change "No"
            # to "yes" if mark_edit_choice == "m".
            with open('tasks.txt', 'w') as file:
                n = 0
                for i in task_data_lists:
                    string = ";".join(i)
                    file.write(string)
                    if n != task_number_list[-1]:
                        file.write("\n")
                        
                    n += 1

            print()
            print(f"Task {task_choice} has been marked as complete.")

        elif mark_edit_choice == "e":

            if task_data_lists[int(task_choice)][5] == "Yes":
                print()
                print(f"Task {task_choice} cannot be edited as it has already been completed!")
            else:
                # print()
                # print(task_data_lists[int(task_choice)])
                print()
                edited_username = input("Please enter the name of the new person assigned to task: ")
                
                # If edited_username does not exist, an error message is printed.
                while edited_username not in username_password.keys():
                    print()
                    print("That user does not exist! Please press b to go back")
                    edited_username = input("to the main menu or enter the name of an existing user: ")
                    if edited_username == "b":
                        break
                
                else:
                    # adds edited_username to task_data_lists to be written
                    # to file later on
                    task_data_lists[int(task_choice)][0] = edited_username

                    # The infinite loop asks for the edited_due_date and if it is in the incorrect
                    # format, the loop will keep giving en error message till the date has been
                    # entered in the correct format.
                    while True:
                        try:
                            edited_due_date = input("Due date of task (YYYY-MM-DD): ")
                            due_date_time = datetime.strptime(edited_due_date, DATETIME_STRING_FORMAT)
                            task_data_lists[int(task_choice)][3] = str(due_date_time.date())
                            break
                        except ValueError:
                            print("Invalid datetime format. Please use the format specified")

                    # The file is re-written with the edited_username and
                    # edited_due_date.
                    with open('tasks.txt', 'w') as file:
                        n = 0
                        for i in task_data_lists:
                            string = ";".join(i)
                            file.write(string)
                            if n != task_number_list[-1]:
                                file.write("\n")
                            
                            n += 1
                    
                    print()
                    print(f"Task {task_choice} succussfully edited!")

def generate_reports():
    '''Creates two files called 'task_overview.txt' and
'user_overview.txt'. 'task_overview' contains information
about the tasks in general and user_overview contains task
information related to specific users. The reports generated
can only be viewed by admin.'''

    # ================== task_overview.txt ===========================

    number_of_tasks = len(task_data_lists)
    
    # The code below prepares certain stastics that are written to file soon after.
    incomplete_and_overdue = 0
    incomplete_time_remaining = 0
    completed = 0
    for i in range(number_of_tasks):
        
        due_date_object = datetime.strptime(task_data_lists[i][3], DATETIME_STRING_FORMAT)
        
        if (due_date_object < datetime.now()) and (task_data_lists[i][5] == "No"):
            incomplete_and_overdue += 1
        elif (due_date_object > datetime.now()) and (task_data_lists[i][5] == "No"):
            incomplete_time_remaining += 1
        else:
            completed += 1
    
    incomplete                        = incomplete_and_overdue + incomplete_time_remaining
    percentage_incomplete             = (incomplete*100)/number_of_tasks
    percentage_incomplete_and_overdue = (incomplete_and_overdue*100)/number_of_tasks

    # Writing to file:
    with open('task_overview.txt', 'w') as file:

        write_string  = ("%-40s %s%s" %("Number of tasks: ", number_of_tasks, "\n"))
        write_string += ("%-40s %s%s" %("Completed: ", completed, "\n"))
        write_string += ("%-40s %s%s" %("Incomplete: ", incomplete, "\n"))
        write_string += ("%-40s %s%s" %("Incomplete and overdue: ", incomplete_and_overdue, "\n"))
        write_string += ("%-40s %s%s" %("Percentage incomplete: ", int(percentage_incomplete), "%\n"))
        write_string += ("%-40s %s%s" %("Percentage incomplete and overdue: ", \
                                        int(percentage_incomplete_and_overdue), "%"))

        file.write(write_string)

    # ================== user_overview.txt ===========================

    # 0 = number of tasks assigned to individual user
    # 1 = percentage of all tasks that are assigned to user
    # 2 = number of tasks assigned to user that have been completed
    # 3 = percentage of tasks assigned to user that have been completed
    # 4 = number of tasks assigned to user that are incomplete with time remaining
    # 5 = percentage of tasks assigned to user that are incomplete but with time remaining
    # 6 = number of tasks assigned to user that are overdue
    # 7 = percentage of tasks assigned to user that are overdue

    # The code below creates a dictionary in username, list pairs.
    # The list will contain statistics regarding the details of each
    # user's tasks.
    user_task_details = {}
    for user in users:
    #   user_task_details[user] = [n, %, n, %, n, %, n, %]   
    #   user_task_details[user] = [0, 1, 2, 3, 4, 5, 6, 7] 
        user_task_details[user] = [0, 0, 0, 0, 0, 0, 0, 0]

    # The for loop concerns itself with the numbers part (signified by the n's) of each list.
    for task in task_data_lists:
        # number of tasks assigned to user
        user_task_details[task[0]][0] += 1

    #   due_date_object = datetime object for the due date of current task in for loop
        due_date_object = datetime.strptime(task[3], DATETIME_STRING_FORMAT)

        if (datetime.now() < due_date_object) and task[5] == "No":
            # incomplete with time remaining
            user_task_details[task[0]][4] += 1
        elif (datetime.now() > due_date_object) and task[5] == "No":
            # incomplete and overdue
            user_task_details[task[0]][6] += 1
        else:
            # completed
            user_task_details[task[0]][2] += 1

    # Here, the numbers from the previous for loop are converted to percentages.
    for user in users:
        try:
            user_task_details[user][1] = int((user_task_details[user][0]*100)/number_of_tasks)
        except ZeroDivisionError:
            user_task_details[user][1] = 0
        try:
            user_task_details[user][3] = int((user_task_details[user][2]*100)/user_task_details[user][0])
        except ZeroDivisionError:
            user_task_details[user][3] = 0
        try:
            user_task_details[user][5] = int((user_task_details[user][4]*100)/user_task_details[user][0])
        except ZeroDivisionError:
            user_task_details[user][5] = 0
        try:
            user_task_details[user][7] = int((user_task_details[user][6]*100)/user_task_details[user][0])
        except ZeroDivisionError:
            user_task_details[user][7] = 0

    # Writing to file:
    with open('user_overview.txt', 'w') as file:
        
        # General task details are written to file here.
        write_string  = ("%-25s %s %s" %("Total number of users: ", len(users), "\n"))
        write_string += ("%-25s %s %s" %("Total number of tasks: ", number_of_tasks, "\n\n"))

        write_string += ("%-25s %s" %("Tasks assigned:", "Total number of tasks assigned to user\n"))
        write_string += ("%-25s %s" %("% tasks assigned: ", "% of all tasks assigned to user\n"))
        write_string += ("%-25s %s" %("% completed: ", "% of tasks assigned to user that are complete\n"))
        write_string += ("%-25s %s" %("% incomplete: ", "% of tasks assigned that are incomplete but with time remaining\n"))
        write_string += ("%-25s %s" %("% overdue: ", "% of tasks assigned that are incomplete and overdue\n\n"))

        file.write(write_string)

        # Task details for each user are written to file here.
        for user in users:
            
            user_string  = ("%-25s %s %s" %("Username: ", user, "\n"))
            user_string += ("%-25s %s %s" %("Tasks assigned: ", user_task_details[user][0], "\n"))
            user_string += ("%-25s %s %s" %("% tasks assigned: ", user_task_details[user][1], "\n"))
            user_string += ("%-25s %s %s" %("% completed: ", user_task_details[user][3], "\n"))
            user_string += ("%-25s %s %s" %("% incomplete: ", user_task_details[user][5], "\n"))
            user_string += ("%-25s %s %s" %("% overdue: ", user_task_details[user][7], "\n\n"))

            file.write(user_string)



#============Main Body==============

while True:
    # Presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit

Option: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        task_addition = add_task()
        if task_addition == True:
            continue

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()
    
    elif menu == 'gr':
        generate_reports()

    elif menu == 'ds' and curr_user != 'admin':
        print("\nThat function is only available to admin.")

    elif menu == 'ds' and curr_user == 'admin':
        '''If the user is an admin, they can display statistics about number of users
            and tasks.'''

        generate_reports()

        print()
        print("-----------------Task Overview----------------\n\n")
        with open('task_overview.txt', 'r') as file:
            for line in file:
                print(line)

        print("\n")
        print("-----------------User Overview----------------\n\n\n")
        with open('user_overview.txt', 'r') as file:
            for line in file:
                print(line)

    elif menu == 'e':
        print('\nGoodbye!!!\n')
        exit()

    else:
        print("You have made the wrong choice, please try again: ")