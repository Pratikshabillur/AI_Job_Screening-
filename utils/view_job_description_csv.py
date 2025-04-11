# File: c:\Users\megha\Downloads\hack\utils\view_job_description_csv.py
import pandas as pd

def view_csv_details(file_path, encodings=None):
    """
    View details of a CSV file with multiple encoding attempts
    """
    if encodings is None:
        encodings = ['utf-8', 'latin-1', 'windows-1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            # Read the CSV file
            df = pd.read_csv(file_path, encoding=encoding)
            
            # Print file details
            print(f"Successfully read with {encoding} encoding")
            print("\n--- CSV File Details ---")
            print(f"Total Rows: {len(df)}")
            print(f"Columns: {list(df.columns)}")
            
            # Print first few rows
            print("\n--- First Few Rows ---")
            print(df.head())
            
            # Print column types
            print("\n--- Column Types ---")
            print(df.dtypes)
            
            return
        except Exception as e:
            print(f"Failed with {encoding} encoding: {e}")
    
    print("Could not read the file with any encoding")

def main():
    file_path = r'c:\Users\megha\Downloads\hack\database\job_description.csv'
    view_csv_details(file_path)

if __name__ == "__main__":
    main()