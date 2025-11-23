# lab3-PersonalExpenseTracker-guymugisha
python summative
Personal Expenses Tracker

This is a lightweight, command-line tool for managing your daily finances. It’s built using Python and a shell script to help you record expenses, monitor your balance, and automatically archive older records.

Project Files

expenses_tracker.py – The main Python program. Lets you view your balance, add expenses, and review your recent entries.

balance.txt – Keeps track of your current balance.

expenses.txt – Stores all new or active expense entries (starts empty).

archive_expenses.sh – A shell script used to archive old expense records and search through previous logs.

archive_log.txt – Keeps a record of every archive action performed.

archives/ – Directory where archived expense files are saved.

How to Use

Ensure Python 3 is installed.

Open your terminal in the project directory.

Start the expense tracker:

python expenses_tracker.py


From the menu, you can check your balance, add new expenses, or view/search recent entries.

To archive old expenses, run:

./archive_expenses.sh


This will:

Move expenses.txt into the archives/ folder with a timestamped filename

Log the archive action in archive_log.txt

Allow you to search archived records by date

Important Notes

Keep expenses.txt in the main directory for adding new expenses.

All older records are automatically stored inside the archives/ folder.

Run archive_expenses.sh frequently to keep your expense history organized and backed up.
