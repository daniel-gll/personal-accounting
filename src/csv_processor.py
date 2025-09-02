# Functions to process CSV files with the bank transactions
import os
import pandas as pd
import banks_format as banks_format
import unified_format as udb
from typing import Dict, List, Optional, Tuple
from utils.utils import log


def load_csv_file(csv_path: str, bank: banks_format.Bank) -> pd.DataFrame:
    """
    Loads a CSV file with specified encodings.
    Args:
        csv_path (str): Path to the CSV file.
        bank (banks_format.Bank): Bank instance for logging purposes.
    Returns:
        pd.DataFrame: Loaded DataFrame from the CSV file.
    Raises:
        FileNotFoundError: If the CSV file does not exist
        ValueError: If the CSV file cannot be decoded with the specified encoding
    """
    # Check if file exists
    if not os.path.exists(csv_path):
        log.error(f"CSV file not found: {csv_path}")
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    try:
        df = pd.read_csv(
            csv_path, 
            delimiter=bank.csv_delimiter, 
            encoding=bank.csv_encoding,
            skiprows=bank.csv_header_row
        )
    except UnicodeDecodeError:
        log.error(f"Failed to load CSV at {csv_path} with delimiter '{bank.csv_delimiter}' and encoding '{bank.csv_encoding}'.")
        raise ValueError(f"Could not decode CSV file: {csv_path}")
      
    log.info(f"Loaded CSV file for {bank} at {csv_path}")
    if bank.csv_header_row > 0:
        log.info(f"Skipped {bank.csv_header_row} header rows")
      
    return df

def print_csv_info(df: pd.DataFrame, bank_name: str):
    """
    Displays general information about the DataFrame, such as number of columns and rows.
    """
    log.info(f"{bank_name} CSV Information:")
    log.info("\t" + f"Columns x rows: {df.shape[1]} x {df.shape[0]}")
    log.info("\t" + f"Column names: {list(df.columns)}")


def validate_csv_headers(df: pd.DataFrame, bank: banks_format.Bank) -> Tuple[List[str], List[str]]:
    """
    Compares DataFrame column headers with bank's header_map.
    Returns a tuple of two lists:
    - Unmatched CSV headers (headers in DataFrame but not in header_map)
    - Unused header_map keys (keys in header_map but not in DataFrame)
    
    Args:
        df (pd.DataFrame): DataFrame containing the CSV data
        bank (Bank): Bank instance containing the header_map
    """
    
    # Check minimum rows
    if len(df) < 5:
        raise ValueError(f"CSV file has only {len(df)} rows. Minimum required: 5 rows")
    
    csv_headers = set(header.strip().lower() for header in df.columns)
    map_headers = set(header.strip().lower() for header in bank.header_map.keys())
    
    # Find headers that exist in CSV but not in header_map
    unmatched_csv = [header for header in df.columns 
                     if header.strip().lower() not in map_headers]

    # Find headers that exist in header_map but not in CSV
    unused_map = [header for header in bank.header_map.keys() 
                  if header.strip().lower() not in csv_headers]

    # Log results
    if unmatched_csv:
        log.warning(f"Unmatched CSV headers: {unmatched_csv}. These headers are in the CSV but not in the bank's header map. They will be ignored.")
    else:
        log.info(f"All CSV headers match the bank's header map.")
    

    
    # TODO hacer checks que las columnas obligarrias hacen match y que todos sus valores estén. Checkear el formato tb
    # # Check that none of the rows in the mandatory columns are blank
    # for col in bank.header_map.values():
    #     if col.mandatory and col.description in csv_headers:
    #         if df[col.description].isnull().all():
    #             raise ValueError(f"All rows are missing values for mandatory column: {col.description}")
       
    # # For description, check if at least one description column has a value
    # if all(df[desc_col].isna().all() for desc_col in desc_cols):
    #     raise ValueError(f"All rows are missing descriptions in columns {desc_cols}")
        
    return unmatched_csv, unused_map



