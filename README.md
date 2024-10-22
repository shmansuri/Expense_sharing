This is a backend application for managing expense sharing among users.
It allows users to create expenses, split them equally, by exact amounts, or by percentage among participants, and track the amounts owed by each user. 
It is built using Django and Django REST Framework.

**Features:**
_Manage Clients_: Create and manage client information.
_Create and Split Expenses_: Create expenses and split them among participants using different methods:
    Equal split
    Exact amounts
    Percentage-based
_Track Expenses_: View expenses for a specific user or download an overall balance sheet.
Download Balance Sheet: Export the balance sheet for an individual user or all users as a CSV file.

**Technology Stack**
    Python (3.10)
    Django (5.0.4)
    Django REST Framework for API management
    SQLite as the default database
    
**Installation**
Clone the repository:

git clone <repository-url>
cd <repository-directory>

Create a virtual environment:

python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate


**Install dependencies:**

pip install -r requirements.txt
Apply migrations:

python manage.py migrate
Create a superuser:

python manage.py createsuperuser

Start the development server:

python manage.py runserver

Access the application:

Open your browser and go to: http://127.0.0.1:8000/
API Endpoints
1. Client Endpoints
Create a Client: POST /api/clients/
List all Clients: GET /api/clients/
Retrieve a Client: GET /api/clients/<id>/
Update a Client: PUT /api/clients/<id>/
Delete a Client: DELETE /api/clients/<id>/
2. Expenses Endpoints
Create an Expense: POST /api/expenses/
Example request body for percentage split:

{
    "description": "Team dinner",
    "total_amount": 1000.00,
    "creator": 1,
    "participants": [2, 3, 4],
    "split_method": "percentage",
    "user_id_1": 2,
    "percentage_1": 50,
    "user_id_2": 3,
    "percentage_2": 25,
    "user_id_3": 4,
    "percentage_3": 25
}
Example request body for equal split:

{
    "description": "Lunch meeting",
    "total_amount": 1200.00,
    "creator": 1,
    "participants": [2, 3, 4],
    "split_method": "equal"
}
List all Expenses: GET /api/expenses/
Retrieve a specific Expense: GET /api/expenses/<id>/
View Expenses for a User: GET /api/expenses/user_expenses/?user_id=<id>
Download Balance Sheet for a User: GET /api/expenses/download_balance_sheet/?user_id=<id>
Download Overall Balance Sheet: GET /api/expenses/download_balance_sheet/
4. Split Detail Endpoints
List all Split Details: GET /api/splitdetails/
Retrieve a specific Split Detail: GET /api/splitdetails/<id>/
Example Usage
Create a Percentage-Based Expense
To create an expense where the amounts are split by percentage, use the following JSON in a POST request to /api/expenses/:

{
    "description": "Office supplies",
    "total_amount": 500.00,
    "creator": 1,
    "participants": [2, 3],
    "split_method": "percentage",
    "user_id_1": 2,
    "percentage_1": 60,
    "user_id_2": 3,
    "percentage_2": 40
}

**Download Balance Sheet**
To download a CSV of the balance sheet for a specific user, use:
GET http://127.0.0.1:8000/api/expenses/download_balance_sheet/?user_id=1

To download a CSV of the overall balance sheet, use:
GET http://127.0.0.1:8000/api/expenses/download_balance_sheet/
