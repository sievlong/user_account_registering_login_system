import time
import string
import easygui as eg
import random
import subprocess

def show_logo():
    subprocess.run(['start', 'logo.ico'], shell=True)

letters = string.ascii_letters  
digits = string.digits  
symbols = string.punctuation  

def generate_user_id():
    return ''.join(random.choices(string.digits, k=4))

def register():
    field_names = ["Username", "Email", "Age", "Gender"]
    field_values = eg.multenterbox("Please enter your information:", "Registration Form", field_names)

    if field_values is None:
        return  

    entered_username = field_values[0]

    with open("accounts.txt", "r") as file:
        for line in file:
            if line.strip():
                _, username, *_ = line.strip().split(" ")
                if entered_username == username:
                    eg.msgbox("User already exists", "Error")
                    return

    email = field_values[1]
    age = field_values[2]
    gender = field_values[3]

    if not all(field_values):
        eg.msgbox("Please fill in all fields", "Error")
        return

    user_id = generate_user_id()

    password = ""
    choice = eg.buttonbox("Do you want to generate a password?", choices=['Yes', 'No', 'Cancel'])
    if choice == "Cancel":
        return  
    elif choice.lower() == "yes":
        msg = "Select password options:"
        title = "Password Options"
        field_names = ["Include digits", "Include symbols", "Password length"]
        field_values = ["no", "no", "10"]
        field_values = eg.multenterbox(msg, title, field_names, field_values)

        if field_values:
            include_digits = field_values[0].lower() == "yes"
            include_symbols = field_values[1].lower() == "yes"
            character_limit = int(field_values[2])

            entered_password = letters
            if include_digits:
                entered_password += digits
            if include_symbols:
                entered_password += symbols

            password = "".join(random.choice(entered_password) for _ in range(character_limit))
            eg.msgbox(f"Your generated password is: {password}", "Generated Password")
    elif choice.lower() == "no":
        entered_password = eg.passwordbox("Enter your password:")
        if entered_password is None:
            return  
        verify_password = eg.passwordbox("Verify password:")
        if verify_password is None:
            return  
        if entered_password == verify_password:
            password = entered_password
        else:
            eg.msgbox("Invalid password", "Error")

    with open("accounts.txt", "a") as store:
        store.write(f'{user_id} {entered_username} {password} {email} {age} {gender}\n')
    
    eg.msgbox("Registration successful. You can now log in.", "Success")



def user_login():
    entered_username = eg.enterbox("Enter your username:")
    if entered_username is None:
        return False, False  

    found_user = False
    with open("accounts.txt", "r") as file:
        for line in file:
            fields = line.strip().split(" ")
            if len(fields) >= 3 and entered_username == fields[1]:
                found_user = True
                break

    if not found_user:
        eg.msgbox("Username not found", "Error")
        return False, False

    entered_password = eg.passwordbox("Enter your password:")
    if entered_password is None:
        return False, False  

    with open("accounts.txt", "r") as file:
        for line in file:
            fields = line.strip().split(" ")
            if len(fields) >= 3 and entered_username == fields[1] and entered_password == fields[2]:
                eg.msgbox("Login successful", "Success")
                return True, fields[0]  

    eg.msgbox("Invalid password", "Error")
    return False, False  


def admin_login():
    entered_username = eg.enterbox("Enter admin username:")
    if entered_username is None:
        return False  
    entered_password = eg.passwordbox("Enter admin password:")
    if entered_password is None:
        return False  

    return entered_username == "admin" and entered_password == "admin"

def display_accounts():
    if not admin_login():
        eg.msgbox("Invalid admin credentials", "Error")
        return

    with open("accounts.txt", "r") as file:
        accounts = file.readlines()

    account_list = "List of User Accounts:\n\n"
    for line in accounts:
        fields = line.strip().split(" ")
        user_id = fields[0]
        username = fields[1]
        password = fields[2]
        email = fields[3] if len(fields) > 3 else ""
        age = fields[4] if len(fields) > 4 else ""
        gender = fields[5] if len(fields) > 5 else ""
        account_list += f'User ID: {user_id} Username: {username:20s} Password: {password} Email: {email} Age: {age} Gender: {gender}\n'

    options = ["Update user info", "Delete a user", "Exit"]
    choice = eg.buttonbox(account_list, "User Accounts List", choices=options)

    if choice == "Delete a user":
        user_to_delete = eg.enterbox("Enter the user ID to delete:")
        if user_to_delete is None:
            return  
        updated_accounts = [line for line in accounts if not line.startswith(user_to_delete + " ")]
        if len(updated_accounts) != len(accounts):
            with open("accounts.txt", "w") as file:
                file.writelines(updated_accounts)
            eg.msgbox(f"User with ID '{user_to_delete}' has been deleted.", "Delete User")
        else:
            eg.msgbox(f"User with ID '{user_to_delete}' not found.", "Delete User")
    elif choice == "Update user info":
        user_id_to_update = eg.enterbox("Enter the user ID to update:")
        if user_id_to_update is None:
            return  
        for i, line in enumerate(accounts):
            if line.startswith(user_id_to_update + " "):
                updated_info = eg.multenterbox("Update user information:", "Update User Info", ["Username", "Password", "Email", "Age", "Gender"], [line.split()[1], line.split()[2], line.split()[3], line.split()[4], line.split()[5]])
                if updated_info is not None:
                    accounts[i] = f"{user_id_to_update} {' '.join(updated_info)}\n"
                    with open("accounts.txt", "w") as file:
                        file.writelines(accounts)
                    eg.msgbox("User information updated successfully.", "Update User Info")
                break

while True:
    choice = eg.buttonbox("User Account Registering Login System",
                          choices=["Register", "Login", "Display User Account List", "Exit"])

    if choice == "Register":
        register()
    elif choice == "Login":
        user_login()
    elif choice == "Display User Account List":
        display_accounts()
    elif choice == "Exit":
        eg.msgbox("Your program will exit in 2 seconds.", "Exiting")
        time.sleep(2)
        eg.msgbox("The 2 seconds are over. Thank you!", "Goodbye")
        break
    else:
        eg.msgbox("Invalid choice. Please try again.", "Error")
