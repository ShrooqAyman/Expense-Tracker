from app.tracker import ExpenseTracker
from app.storage import StorageService
from datetime import date

if __name__ == "__main__":
    storage = StorageService("data/expenses.json")
    tracker = ExpenseTracker(storage)

    while True:
        print("\nWhat would you like to do?")
        print("1. Add Expense")
        print("2. Update Expense")
        print("3. Delete Expense")
        print("4. List Expenses")
        print("5. List Expenses for catgory")
        print("6. Show total summary")
        print("7. Show month summary")
        print("8. Set month budget")
        print("9. Exit")

        choice = input("Enter choice (1-9): ")

        if choice == "1":
            desc = input("Description: ")
            amt = float(input("Amount: "))
            cat = input("Category (optional): ")
            tracker.add_expense(desc, amt, cat if cat else None)

        elif choice == "2":
            try:
                eid = int(input("Enter Expense ID to update: "))
                desc = input("New Description (leave blank to skip): ")
                amt_input = input("New Amount (leave blank to skip): ")
                amt = float(amt_input) if amt_input else None
                cat = input("New Category (leave blank to skip): ")
                tracker.update_expense(eid, description=desc or None, amount=amt, category=cat or None)
            except ValueError:
                print("❌ Invalid input.")

        elif choice == "3":
            try:
                eid = int(input("Enter Expense ID to delete: "))
                tracker.delete_expense(eid)
            except ValueError:
                print("❌ Invalid ID.")

        elif choice == "4":
            tracker.list_expenses()

        elif choice == "5":
            try:
                category = input("Enter category name to list expense: ")
                tracker.list_expenses(category)
            except ValueError:
                print("❌ Invalid category.")
        elif choice == "6":
            total_expense = tracker.get_expenses_summary()
            print(f"Total expenses : {total_expense}$")
        elif choice == "7":
            try:
                month = int(input("Enter month to show total expense: "))
                total_expense = tracker.get_expenses_summary(month)
            except ValueError:
                print("❌ Invalid month.")
            print(f"Total expenses : {total_expense}$")

        elif choice == "8":
            try:
                month = input("Enter month: ")
                budget = float(input("Enter month budget: "))
                result = tracker.set_monthly_budget(month, budget)
                if result[0]:
                    print(result[1])
                else:
                    print("Errors:")
            except ValueError:
                print("❌ Invalid month.")
            

        elif choice == "9":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter a number from 1 to 5.")
