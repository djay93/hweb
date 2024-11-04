# Task Management Application

This is a Flask-based Task Management application that allows users to create, view, and execute tasks. It's designed with a modular structure, making it suitable for production and enterprise-grade environments.

## Features

- Dashboard to view all tasks
- Add new tasks
- Task overview with execution history
- Execute and re-execute tasks
- Logging system for production use
- Modular structure for easy maintenance and scalability

## Prerequisites

- Python 3.9+
- pip (Python package manager)

## Installation

1. Clone the repository:   ```
   git clone https://github.com/yourusername/task-management-app.git
   cd task-management-app   ```

2. Create a virtual environment and activate it:   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`   ```

3. Install the required packages:   ```
   pip install -r requirements.txt   ```

4. Set up environment variables (optional):   ```
   export FLASK_APP=run.py
   export FLASK_ENV=development
   export SECRET_KEY=your_secret_key
   export DATABASE_URL=sqlite:///tasks.db   ```

5. Initialize the database:   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade   ```
   flask seed-db

## Running the Application

To run the application in development mode:
flask run