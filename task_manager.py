# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# # program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            data = file.read().split("\n")
            return [entry for entry in data if entry != ""]
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading '{file_name}': {e}")
        return []

# Usage
task_data = read_file("tasks.txt")
user_data = read_file("user.txt")

task_list = []

for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''

try:
    # Check if the file exists
    if not os.path.exists("user.txt"):
        # If it doesn't exist, create it with a default account
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")
    else:
        # If the file already exists, you might want to handle this case accordingly
        print("User file already exists. No action taken.")
except Exception as e:
    print(f"An error occurred: {e}")

try:
    # Read in user_data
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

except FileNotFoundError:
    print("Error: File 'user.txt' not found.")
    # Handle the absence of the file in a way that makes sense for your application.
    # You might want to create the file or provide a default user_data.

except Exception as e:
    print(f"An error occurred while reading 'user.txt': {e}")
    # Handle other exceptions, providing feedback or taking appropriate actions.

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

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



def reg_user():
    '''Register a new user to the user.txt file (only accessible by admin).
    Ensures that duplicate usernames are not added. 
    '''

    if curr_user != 'admin':
        print("Only admin can register new users.")
        return

    # Request input for a new username
    new_username = input("New Username: ")

    # Validate that the username is not empty
    while new_username == "":
        new_username= input("Username cannot be empty. Please enter a valid username: ")
    # Validate that the username is not repeated
    while new_username in username_password.keys():
        new_username = input("This username already exists. Please enter another username: ")

    # - Request input of a new password
    new_password = input("New Password: ")

    # Validate that the password is not empty
    while new_password == "":
        new_password = input("Password cannot be empty. Please enter a valid password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Otherwise you present a relevant message and ask again.
    while confirm_password != new_password:
        print("Passwords do not match. Please try again.")
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added.")
        username_password[new_username] = new_password
            
        with open("user.txt", "w") as out_file:
            user_data = []
            user_data = [f"{username};{password}" for username, password in username_password.items()]
            out_file.write("\n".join(user_data))

def add_task():
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task.'''

    if curr_user != 'admin':
            print("Only admin can add tasks.")
            return

    task_username = input("Name of person assigned to task: ")
    while task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        task_username = input("Name of person assigned to task: ")

    # Validate Task Title
    while True:
        task_title = input("Title of Task: ")
        if task_title.strip():  # Check if the title is not empty after stripping whitespaces
            break
        else:
            print("Task title cannot be empty. Please enter a valid title.")

    # Validate Task Description
    while True:
        task_description = input("Description of Task: ")
        if task_description.strip():  # Check if the description is not empty after stripping whitespaces
            break
        else:
            print("Task description cannot be empty. Please enter a valid description.")

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            if due_date_time < datetime.combine(date.today(), datetime.min.time()):
                print("This day has passed. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    existing_task = next((t for t in task_list if t['title'] == task_title and t['username'] == task_username), None)

    if existing_task:
        print("A task with the same title and assigned user already exists. Cannot add duplicate tasks.")
        return

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

    task_list.append(new_task)

    with open("tasks.txt", "a") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_line = ";".join(str_attrs)
            task_file.write(task_line + "\n")

        print("Task successfully added.")


def view_all():
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''
        print("Here is a list of all the tasks:\n" + ("-" * 50))
        for t in task_list:
            disp_str = f"\x1B[4;1mTask:\033[0m \t\t {t['title']}\n" # Underlined and made bold
            disp_str += f"\033[1mAssigned to:\033[0m \t {t['username']}\n"  # Made bold
            disp_str += f"\033[1mDate Assigned:\033[0m \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"  # Made bold
            disp_str += f"\033[1mDue Date:\033[0m \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"  # Made bold
            disp_str += f"\033[1mStatus:\033[0m \t {'Completed' if t['completed'] else 'Incomplete'}\n"  # Made bold
            disp_str += f"\033[1mTask Description:\033[0m \n{t['description']}\n"   # Made bold
            disp_str += ("-" * 50)
            print(disp_str)

def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
    '''
    for index, task in enumerate([t for t in task_list if t['username'] == curr_user], start=1):
        disp_str = f"\x1B[4;1mTask {index}\033[0m\n"    # Underlined and made bold 
        disp_str += f"\033[1mTitle:\033[0m \t\t {task['title']}\n"  # Made bold
        disp_str += f"\033[1mAssigned to:\033[0m \t {task['username']}\n"   # Made bold
        disp_str += f"\033[1mDate Assigned:\033[0m \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"   # Made bold
        disp_str += f"\033[1mDue Date:\033[0m \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n" # Made bold
        disp_str += f"\033[1mStatus:\033[0m \t {'Completed' if task['completed'] else 'Incomplete'}\n"  # Made bold
        disp_str += f"\033[1mTask Description:\033[0m \n{task['description']}\n"    # Made bold
        disp_str += "-" * 50  # Add a line of dashes for separation
        print(disp_str)

    selection = int(input("Please enter the number of the task you want to edit or enter '-1' to return to the main menu: "))
    for index, task in enumerate([t for t in task_list if t['username'] == curr_user], start=1):
        if selection == index and task['completed'] == False:
            changes = int(input("""Your options:\n1. Mark task complete
2. Assign task to someone else\n3. Change the due date\n
Please enter your selection: """))
            if changes == 1:
                task['completed'] = True
                with open('tasks.txt', 'r') as file:
                    lines = file.readlines()
                # Modify the specific line in memory
                for i, line in enumerate(lines):
                    if task['title'] in line and task['username'] == curr_user:
                        lines[i] = line.replace(';No', ';Yes')
                        break
                # Write all the modified lines back to the file
                with open('tasks.txt', 'w') as file:
                    file.writelines(lines)
                print("This task is now complete.")
            elif changes == 2:
                new_assign = input("Please enter the username you would like to assign this task to: ")
                while new_assign not in username_password.keys():
                    new_assign = input("This username doesn't exist. Please enter again: ")

                # Find the task in the task_list and update its username
                for t in task_list:
                    if t['title'] == task['title'] and t['username'] == curr_user:
                        t['username'] = new_assign

                # Update the tasks.txt file
                with open('tasks.txt', 'r') as file:
                    lines = file.readlines()

                with open('tasks.txt', 'w') as file:
                    for line in lines:
                        task_components = line.split(";")
                        if task_components[1] == task['title'] and task_components[0] == curr_user:
                            # Replace the old username with the new one
                            line = line.replace(curr_user, new_assign)
                        file.write(line)
                print("Task successfully assigned.")
            elif changes == 3:
                while True:
                    try:
                        new_due_date = input("Enter the new due date of task (YYYY-MM-DD): ")
                        due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                        if due_date_time < datetime.combine(date.today(), datetime.min.time()):
                            print("This day has passed. Please try again.")
                        else:
                            for t in task_list:
                                if t['title'] == task['title'] and t['username'] == curr_user:
                                    t['due_date'] = due_date_time

                            # Read all lines from the file, modify the relevant line, and write back
                            with open('tasks.txt', 'r') as file:
                                lines = file.readlines()

                            with open('tasks.txt', 'w') as file:
                                for line in lines:
                                    task_components = line.split(";")
                                    if task_components[1] == task['title'] and task_components[0] == curr_user:
                                        # Replace the old due date with the new one
                                        line = line.replace(t['due_date'].strftime(DATETIME_STRING_FORMAT), due_date_time.strftime(DATETIME_STRING_FORMAT))
                                    file.write(line)
                            print("The due date has been changed.")
                            break
                    except ValueError:
                        print("Invalid datetime format. Please use the format specified")
        elif selection == index and task['completed'] == True:
            print("Sorry, this task cannot be modified, as it is complete.")

def task_oview(task_list):
    '''
    Creates a text file with the overview of users.
    '''
    total_tasks = len(task_list)
    total_comp_tasks = sum(1 for task in task_list if task['completed'])
    total_incomp_tasks = total_tasks - total_comp_tasks
    incomp_overdue_total = sum(1 for task in task_list if not task['completed'] and task['due_date'] < datetime.combine(date.today(), datetime.min.time()))
    incomp_percent = (total_incomp_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    overdue_percent = (incomp_overdue_total / total_incomp_tasks) * 100 if total_incomp_tasks > 0 else 0
    
    with open('task_overview.txt', 'w') as file:
        file.write("Task overview of users\n")
        file.write(f"The total number of tasks on the program: {total_tasks}\n")
        file.write(f"The total number of completed tasks: {total_comp_tasks}\n")
        file.write(f"The total number of incomplete tasks: {total_incomp_tasks}\n")
        file.write(f"The total number of overdue tasks: {incomp_overdue_total}\n")
        file.write(f"Percentage of incomplete tasks: {round(incomp_percent, 2)}%\n")
        file.write(f"Percentage of overdue and incomplete tasks: {round(overdue_percent, 2)}%\n")

def all_users_task_statistics(task_list):
    '''
    Creates a text file with the statistics of users.
    '''
    all_users = set(task['username'] for task in task_list)
    with open('user_overview.txt', 'w') as user_file:
        user_file.write("User overview of each user\n")
        for curr_user in all_users:
            total_user_tasks = sum(1 for task in task_list if task['username'] == curr_user)
            total_tasks = len(task_list)

            user_file.write(f"\nUser: {curr_user}\n")
            user_file.write(f"Total tasks assigned to {curr_user}: {total_user_tasks}\n")

            if total_tasks > 0:
                user_tasks_percent = (total_user_tasks / total_tasks) * 100
                user_tasks_percent = round(user_tasks_percent, 2)
                user_file.write(f"Percentage of total tasks: {user_tasks_percent}%\n")

                user_comp_total = sum(1 for task in task_list if task['completed'] and task['username'] == curr_user)
                user_comp_percent = (user_comp_total / total_user_tasks) * 100
                user_comp_percent = round(user_comp_percent, 2)
                user_file.write(f"{curr_user} has completed {user_comp_percent}% of their tasks.\n")

                user_incomp_total = total_user_tasks - user_comp_total
                user_incomp_percent = (user_incomp_total / total_user_tasks) * 100
                user_incomp_percent = round(user_incomp_percent, 2)
                user_file.write(f"{user_incomp_percent}% of {curr_user} tasks are incomplete.\n")


                user_incomp_overdue = sum(1 for task in task_list if not task['completed'] and task['username'] == curr_user and task['due_date'] < datetime.combine(date.today(), datetime.min.time()))
                user_overdue_percent = (user_incomp_overdue / total_user_tasks) * 100
                user_overdue_percent = round(user_overdue_percent, 2)
                user_file.write(f"{user_overdue_percent}% of {curr_user} tasks are overdue.\n")
            else:
                print(f"No tasks available for {curr_user}.")

def generate_reports():
    '''Generate reports (only accessible by admin).'''
    if curr_user != 'admin':
        print("Only admin can generate reports.")
        return

    task_oview(task_list)
    all_users_task_statistics(task_list)
    print("Reports generated in task_overview.txt and user_overview.txt.")

while logged_in == True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
gr - Generate reports                 
ds - Display statistics
e - Exit
: ''').lower()
    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'gr':
        generate_reports()
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, please try again")