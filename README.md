# Python Database Integration Project

This project connects to a PDF file, extracts data, and inserts it into a SQL Server database. It demonstrates how to use Python to work with SQL using `pyodbc`, as well as how to parse data from PDFs using the `fitz` library (part of PyMuPDF).

## Requirements

- Python 3.x
- `pyodbc` for database connection
- `PyMuPDF` (`fitz`) for reading and extracting data from PDF files
- `re` for regular expression-based data extraction
- `configparser` for reading configuration files
- `datetime` for logging timestamps

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/shivampuninani/integration_pdf_sql.git

   
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt

3. Configure the database connection:

Update the connection details in the config.ini file with your SQL Server credentials. Here's the format:
   [database]
   server = SQLEXPRESS  
   database = Test_Database  
   username = sa  
   password = 12345678  

Update the connection strings (if required) in Python_PDF_to_SQL.py for both SQL Server and Excel file handling.
SQL Server: Update the SERVER, DATABASE, UID, and PWD placeholders in the config.ini file.
Excel File: Ensure the path to your PDF file is correct in the Python_PDF_to_SQL.py script.

4. Run the script:
   ```bash
   python Python_PDF_to_SQL.py


EXCEL-SQL-Integration-project/  
│  
├── Python_PDF_to_SQL.py               # Your main Python program  
├── requirements.txt                     # Python dependencies  
├── README.md                            # Project documentation  
├── config.ini                           # config file to store and configure sql server and file data   
├── .gitignore                           # Git ignore rules  
└── log_file.txt                         # Log file (will be generated when running the program)  
