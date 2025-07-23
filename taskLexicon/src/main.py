from email_service import EmailService
from dictionary import generate_dictionary

def get_user_input():
    """
    Prompt the user to enter task details and email address.
    """
    print("Please enter the following details:")
    task_name = input("Task Name: ")
    task_description = input("Task Description: ")
    email_address = input("Recipient Email Address: ")

    return task_name, task_description, email_address

def main():
    task_name, task_description, email_address = get_user_input()

    email_service = EmailService()

    dictionary_content = generate_dictionary(task_name, task_description)

    email_service.send_email(email_address, f'Task Lexicon: {task_name}', dictionary_content)

    print("Dictionary content generated successfully.")


if __name__ == "__main__":
   main()