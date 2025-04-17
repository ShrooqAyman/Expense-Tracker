 # <a href="https://roadmap.sh/projects/expense-tracker">🧾 Expense Tracker CLI </a>

A simple command-line Expense Tracker application to help you manage your finances. Add, update, delete, and view expenses, set monthly budgets, and export data to CSV — all from your terminal!

---

## 🚀 Features

- Add a new expense with a description, amount, and optional category.
- Update existing expenses.
- Delete expenses by ID.
- View all expenses in a readable table.
- Filter expenses by category.
- Get a total summary of expenses.
- View a monthly summary of expenses.
- Set monthly budgets and receive warnings when exceeded.
- Export expenses to a CSV file.

---

## 🛠️ Technologies Used

- Python 3.x
- `argparse` for CLI argument parsing
- `json` for data storage
- `prettytable` for nicely formatted tables
- `csv` for exporting data

---

## 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/expense-tracker-cli.git
   ```
   ```bash
   cd expense-tracker
   ```
## 🧠 Implementation Notes
- Data is stored in JSON format under the data/expenses.json and data/budget.json files.

- Each expense includes: id, description, amount, category, and date.

- All user input is validated to prevent issues like negative values or missing fields.

- Budget warnings are shown automatically when monthly expenses exceed the set budget.

## 📁 Project Structure
bash
Copy
Edit

```bash
expense-tracker/
│
├── app/
│   ├── tracker.py           # Main logic for handling expenses
│   ├── storage.py           # File I/O and persistence
│   ├── validator.py         # Input validation logic
│
├── models/
│   ├── Expense.py           # Expense class model
│   ├── budget_service.py    # Budget management
│
├── data/                    # JSON storage files
│   ├── expenses.json
│   ├── budget.json
│
├── main.py                  # CLI entry point using argparse
├── README.md                # Project documentation
├── requirements.txt         # Required Python packages
```
