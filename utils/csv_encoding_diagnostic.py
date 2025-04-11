# File: c:\Users\megha\Downloads\hack\utils\csv_encoding_diagnostic.py
import pandas as pd
import chardet
import os

def detect_file_encoding(file_path):
    """
    Detect the encoding of a file using chardet
    """
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        print(f"Detected encoding: {result['encoding']} (Confidence: {result['confidence']})")
    
    return result['encoding']

def try_read_csv(file_path, encodings=None):
    """
    Try reading CSV with different encodings
    """
    if encodings is None:
        encodings = ['utf-8', 'latin-1', 'windows-1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            print(f"Successfully read with {encoding} encoding")
            print("DataFrame Info:")
            print(df.info())
            print("\nFirst few rows:")
            print(df.head())
            return df
        except Exception as e:
            print(f"Failed with {encoding} encoding: {e}")
    
    print("Could not read the file with any of the specified encodings.")
    return None

def diagnose_problematic_character(file_path, encoding='utf-8'):
    """
    Diagnose the problematic character causing encoding issues
    """
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
        
        # Try to decode and find the problematic character
        try:
            content.decode(encoding)
        except UnicodeDecodeError as e:
            print(f"Problematic character details:")
            print(f"Error: {e}")
            print(f"Problematic byte: {content[e.start:e.end]}")
            print(f"Surrounding context: {content[max(0, e.start-10):min(len(content), e.end+10)]}")
    except Exception as e:
        print(f"Error reading file: {e}")

def main():
    file_path = r'c:\Users\megha\Downloads\hack\database\job_description.csv'
    
    # File existence and size check
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist!")
        return
    
    file_size = os.path.getsize(file_path)
    print(f"File size: {file_size} bytes")
    
    # First, detect the encoding
    detected_encoding = detect_file_encoding(file_path)
    
    # Diagnose problematic character
    diagnose_problematic_character(file_path)
    
    # Then try reading with the detected and other common encodings
    try_read_csv(file_path, [detected_encoding, 'utf-8', 'latin-1', 'windows-1252'])

if __name__ == "__main__":
    main()