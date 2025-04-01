from colorama import Fore, Style


def show_menu():
    """
    Display the main menu options to the user.
    This function prints a numbered list of available actions,
    allowing the user to choose which set of calendar events they
    want to view or to access the daily reminder configuration.

    Menu options include:
        1 - Show today's appointments
        2 - Show tomorrow's appointments
        3 - Show appointments for the week
        4 - Show the next appointment
        5 - Configure daily reminder settings
    """
    print("\n📱WhatsApp Calendar Menu")
    print("1️⃣ Today's appointments")
    print("2️⃣ Tomorrow's appointments")
    print("3️⃣ Appointments for the week")
    print("4️⃣ Next appointment")
    print("5️⃣ Daily reminder configuration")

def main():
    """
    Entry point of the WhatsApp Calendar.

    This function initializes a continuous loop that:
        - displays the menu to the user
        - accepts a numeric input
        - calls the corresponding function from the services module

    It ensures valid input and guides the user through the available
    features step by step.
    """
    valid_choices = {'1', '2', '3', '4', '5'}

    show_menu()
    choice = input("Enter a number 1-5 to select an option: ")

    while True:
        if choice in valid_choices:
            if choice == '1':
                pass
                show_menu()
            elif choice == '2':
                pass
                show_menu()
            elif choice == '3':
                pass
                show_menu()
            elif choice == '4':
                pass
                show_menu()
            elif choice == '5':
                pass
                show_menu()
            else:
                print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
                show_menu()


if __name__ == "__main__":
    show_menu()
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram terminated by user." + Style.RESET_ALL)