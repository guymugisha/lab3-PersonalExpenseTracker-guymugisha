import sys
from datetime import datetime

COLOR_SUCCESS = "\033[92m"
COLOR_ERROR = "\033[91m"
COLOR_WARNING = "\033[93m"
COLOR_INFO = "\033[96m"
COLOR_RESET = "\033[0m"

def show_intro():
    print("="*40)
    print(f"{COLOR_INFO}      DAILY BUDGET MANAGER      {COLOR_RESET}")
    print("="*40)
    print("Welcome! Track your spending with ease.\n")

def display_balance():
    try:
        with open("balance.txt", "r") as balance_file:
            saved_balance = float(balance_file.read().strip())
    except FileNotFoundError:
        print(f"{COLOR_WARNING}balance.txt not found! Initializing balance to 0.{COLOR_RESET}")
        saved_balance = 0.0

    total_spent = 0.0
    try:
        with open("expenses.txt", "r") as expense_file:
            for entry in expense_file:
                fields = entry.strip().split("|")
                if len(fields) == 5:
                    total_spent += float(fields[4].strip())
    except FileNotFoundError:
        total_spent = 0.0

    remaining_funds = saved_balance - total_spent

    print("\n" + "="*15 + " BALANCE SUMMARY " + "="*15)
    print(f"Saved Balance     : ${saved_balance:.2f}")
    print(f"Total Spent       : ${total_spent:.2f}")
    print(f"Remaining Funds   : ${remaining_funds:.2f}")
    print("="*45 + "\n")

    update_choice = input("Would you like to add funds? (y/n): ").strip().lower()
    if update_choice == "y":
        while True:
            try:
                deposit = float(input("Enter amount to add: ").strip())
                if deposit <= 0:
                    print(f"{COLOR_ERROR}Amount must be positive.{COLOR_RESET}")
                    continue
                saved_balance += deposit
                with open("balance.txt", "w") as balance_file:
                    balance_file.write(f"{saved_balance:.2f}")
                print(f"{COLOR_SUCCESS}Balance updated! New total: ${saved_balance:.2f}{COLOR_RESET}\n")
                break
            except ValueError:
                print(f"{COLOR_ERROR}Invalid input. Please enter a number.{COLOR_RESET}")

def record_expense():
    try:
        with open("balance.txt", "r") as balance_file:
            balance_data = balance_file.read().strip()
            saved_balance = float(balance_data) if balance_data else 0.0
    except FileNotFoundError:
        saved_balance = 0.0

    total_spent = 0.0
    try:
        with open("expenses.txt", "r") as expense_file:
            for entry in expense_file:
                fields = entry.strip().split("|")
                if len(fields) == 5:
                    total_spent += float(fields[4].strip())
    except FileNotFoundError:
        total_spent = 0.0

    remaining_funds = saved_balance - total_spent
    print(f"\nAvailable funds: ${remaining_funds:.2f}\n")

    while True:
        expense_date = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(expense_date, "%Y-%m-%d")
            break
        except ValueError:
            print(f"{COLOR_ERROR}Invalid format! Use YYYY-MM-DD.{COLOR_RESET}")

    expense_name = input("Enter item name: ").strip()

    while True:
        try:
            expense_cost = float(input("Enter amount spent: ").strip())
            if expense_cost <= 0:
                print(f"{COLOR_ERROR}Amount must be positive.{COLOR_RESET}")
                continue
            if expense_cost > remaining_funds:
                print(f"{COLOR_ERROR}Not enough balance! Expense not recorded.{COLOR_RESET}\n")
                return
            break
        except ValueError:
            print(f"{COLOR_ERROR}Invalid input. Please enter a number.{COLOR_RESET}")

    expense_number = 1
    try:
        with open("expenses.txt", "r") as expense_file:
            entries = expense_file.readlines()
            if entries:
                last_entry = entries[-1]
                expense_number = int(last_entry.split("|")[0].strip()) + 1
    except FileNotFoundError:
        pass

    current_time = datetime.now().strftime("%H:%M")

    with open("expenses.txt", "a") as expense_file:
        expense_file.write(f"{expense_number} | {expense_date} | {current_time} | {expense_name} | {expense_cost:.2f}\n")

    print(f"{COLOR_SUCCESS}🎉 Expense recorded! New balance: ${remaining_funds - expense_cost:.2f}{COLOR_RESET}\n")

def search_expenses():
    try:
        with open("expenses.txt", "r") as expense_file:
            entries = expense_file.readlines()
            if not entries:
                print(f"\n{COLOR_WARNING}No expenses recorded yet.{COLOR_RESET}\n")
                return
    except FileNotFoundError:
        print(f"\n{COLOR_WARNING}No expense file found.{COLOR_RESET}\n")
        return

    while True:
        print("\nEXPENSE SEARCH")
        print("1. Search by item name")
        print("2. Search by amount")
        print("3. Return to main menu")

        search_choice = input("Choose an option (1-3): ").strip()

        if search_choice == "1":
            keyword = input("Enter item name: ").strip().lower()
            print(f"\n=== RESULTS ===")
            match_found = False
            for entry in entries:
                fields = entry.strip().split("|")
                if len(fields) == 5 and keyword in fields[3].strip().lower():
                    print(f"ID: {fields[0]}, Date: {fields[1]}, Time: {fields[2]}, Item: {fields[3]}, Amount: ${fields[4]}")
                    match_found = True
            if not match_found:
                print(f"{COLOR_WARNING}No matching items found.{COLOR_RESET}")
        elif search_choice == "2":
            try:
                target_amount = float(input("Enter amount: ").strip())
                print("\n=== RESULTS ===")
                match_found = False
                for entry in entries:
                    fields = entry.strip().split("|")
                    if len(fields) == 5 and float(fields[4].strip()) == target_amount:
                        print(f"ID: {fields[0]}, Date: {fields[1]}, Time: {fields[2]}, Item: {fields[3]}, Amount: ${fields[4]}")
                        match_found = True
                if not match_found:
                    print(f"{COLOR_WARNING}No matching amounts found.{COLOR_RESET}")
            except ValueError:
                print(f"{COLOR_ERROR}Invalid amount. Please enter a number.{COLOR_RESET}")
        elif search_choice == "3":
            return
        else:
            print(f"{COLOR_ERROR}Invalid choice. Please enter 1, 2, or 3.{COLOR_RESET}")

def launch_menu():
    while True:
        print("\nMAIN MENU")
        print("1. View Balance")
        print("2. Search Expenses")
        print("3. Record Expense")
        print("4. Exit")

        user_choice = input("Choose an option (1-4): ").strip()

        if user_choice == "1":
            display_balance()
        elif user_choice == "2":
            search_expenses()
        elif user_choice == "3":
            record_expense()
        elif user_choice == "4":
            print(f"\n{COLOR_INFO}Thanks for using Daily Budget Manager. Goodbye! 👋{COLOR_RESET}")
            sys.exit()
        else:
            print(f"{COLOR_ERROR}Invalid choice. Please enter 1, 2, 3, or 4.{COLOR_RESET}")

if __name__ == "__main__":
    show_intro()
    launch_menu()