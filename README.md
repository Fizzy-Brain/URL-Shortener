# URL Shortener

A simple URL shortener application built with Python.

## Features

- Shorten long URLs to more manageable links
- Store and manage shortened URLs in a database
- Simple and intuitive interface

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd shorten-url
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

## Project Structure

- `main.py`: Main application file
- `db_connection.py`: Database connection and operations
- `schema.py`: Database schema definitions
