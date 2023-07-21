import sys
from models import Administrator
from views.menu_view import display_message
import re
from sqlalchemy.exc import SQLAlchemyError


def ask_to_create_admin():
    while True:
        display_message("Currently, no administrator exists on the database. You need at least one to use the app. Do you want to create an administrator now?")
        try:
            ask_select_choice = int(input(display_message("Select 1 for Yes or 2 for No: ")))
            if ask_select_choice == 1:
                answer_create_choice = True
                break
            elif ask_select_choice == 2:
                answer_create_choice = False
                break
            else:
                display_message("Invalid choice. Please try again.")
        except ValueError:
            display_message("Invalid input. Please enter a valid choice.")

    return answer_create_choice


def form_first_admin():
    while True:
        surname = str(input(display_message("Enter the surname of the first administrator: ")))
        if not surname.isalpha():
            display_message("Surname should only contain alphabetic characters. Please try again.")
        else:
            break

    while True:
        lastname = str(input(display_message("Enter the lastname of the first administrator: ")))
        if not lastname.isalpha():
            display_message("Lastname should only contain alphabetic characters. Please try again.")
        else:
            break

    while True:
        try:
            age = int(input(display_message("Enter the age of the first administrator: ")))
            break
        except ValueError:
            display_message("Invalid input. Please enter a valid age.")

    while True:
        email = input(display_message("Enter the email address of the first administrator: "))
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            display_message("Email address is not valid. Please try again.")
        else:
            break

    while True:
        password = str(input(display_message("Enter the password for the first administrator: ")))
        if len(password) < 6:
            display_message("Password should be at least 6 characters long. Please try again.")
        elif not password.isalnum():
            display_message("Password should only contain alphanumeric characters. Please try again.")
        else:
            break

    return surname, lastname, age, email, password


def create_first_administrator():
    if ask_to_create_admin():
        surname, lastname, age, email, password = form_first_admin()
        try:
            administrator = Administrator.create(surname, lastname, age, email, password)
            display_message(f"Administrator created: {administrator}")
        except SQLAlchemyError as e:
            display_message(str(e))
    else:
        display_message("Come back to create the first admin later")
        sys.exit(1)
