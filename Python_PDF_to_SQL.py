import pyodbc, os, shutil
import fitz
import re
from datetime import datetime
import configparser



def get_db_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    db_config = {
        'server': config.get('database', 'server'),
        'database': config.get('database', 'database'),
        'username': config.get('database', 'username'),
        'password': config.get('database', 'password'),
        'filePath': config.get('fileData', 'filePath'),
        'filePrefix': config.get('fileData', 'filePrefix'),
        'fileSuccessPath' : config.get('fileData', 'fileSuccessPath'),
        'fileErrorPath' : config.get('fileData', 'fileErrorPath'),
    }
    return db_config


def db_connection(server, database, uid, pwd):
    
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={uid};'
        f'PWD={pwd}'
    )
    return conn


def extract_value_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    full_text = ""
    print(len(pdf_document))
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        print(page)
        full_text += page.get_text()

    pdf_document.close()

    return full_text


def push_to_sql():
    db_config = get_db_config()
    conn = db_connection(db_config["server"], db_config["database"], db_config["username"], db_config["password"])
    cursor = conn.cursor()
        
    #print(rows)
    filepath = db_config["filePath"] + "\\" + "PDF_Test_File.pdf"
    rows = extract_value_from_pdf(filepath)
    test_no_track = ''

    try:
        ID = (re.findall(r'ID(\d):\s*(\w+)',rows))
        
        ID_F = (re.findall(r'ID(\d)_F(\d):\s*(\w+)',rows))
        
        ID_status = (re.findall(r'ID(\d)_status:\s*(\w+)',rows)[0])

        for id in ID:
            print(id[1])
            print(ID_F[int(id[0])*3 - 3][2])
            print(ID_F[int(id[0])*3 - 2][2])
            print(ID_F[int(id[0])*3 - 1][2])
            cursor.execute('''INSERT INTO [dbo].[Test_PDF]
                                ([ID]  ,[Field1] ,[Field_data1] ,[Field2] ,[Field_data2] ,[Field3] ,[Field_data3], timestamp)
                           VALUES (  ?,          ?,               ?,                           ?,               ?,                       ?,            ?,            getdate())'''.format(length='multi-line', ordinal='second'),
                                    id[1]  ,id[1]+'_F1' , ID_F[int(id[0])*3 - 3][2] ,id[1]+'_F2' ,ID_F[int(id[0])*3 - 2][2] ,id[1]+'_F3' ,ID_F[int(id[0])*3 - 1][2])
        log_report(test_no_track, "success")
    except Exception as e:
            log_report(test_no_track, e)
            #continue
    
    conn.commit()   # sql connection closed
    conn.close()

def log_report(test_no_track, e):
    # log_file = 'log.txt'
    log_file = r".\log_file.txt"
    with open(log_file, 'a') as log:
        log.write(f"{datetime.now()} + ' | ' +  {test_no_track} + ' | ' +  {e} \n")

if __name__ == "__main__":
    with open("log_file.txt", "w") as log: print("start", file = log)
    
    #print(rows)
    push_to_sql()
    #print("Datan Inserted in db Successfully.")  
