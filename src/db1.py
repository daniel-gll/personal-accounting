# Functions to process CSV files with the bank transactions
import pandas as pd
import banks_format as banks_format
import unified_format as udb

def load_csv_file(csv_path, bank):
    
    """
    Loads a CSV file with specified encodings.
    Args:
        csv_path (str): Path to the CSV file.
        bank_name (str): Name of the bank for logging purposes.
    Returns:
        pd.DataFrame: Loaded DataFrame from the CSV file.
    """
    try:
        df = pd.read_csv(
            csv_path, 
            delimiter=bank.cvs_delimiter, 
            encoding=bank.csv_encoding,
            skiprows=bank.cvs_header_row
        )
    except UnicodeDecodeError:
        print(f"Error! Failed to load csv with at {csv_path} with delimiter {bank.cvs_delimiter} and encoding {bank.csv_encoding}.")
        raise ValueError(f"Could not decode csv file: {csv_path}")
      
    print(f"Loaded CSV file for {bank} at {csv_path}")
    if bank.cvs_header_row > 0:
        print(f"Skipped {bank.cvs_header_row} header rows")
    
    # Validate headers
    unmatched_csv, unused_map = _compare_headers(df, bank)
    
    # Validate DataFrame contents
    _validate_dataframe(df, bank)
    
    return df

def _validate_dataframe(df, bank):
    """
    Validates DataFrame contents according to bank requirements.
    Checks for required columns, minimum rows, and missing values.
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        bank (Bank): Bank instance containing validation rules
        
    Raises:
        ValueError: If validation fails
    """
    # Get required column names from header_map
    date_col = next((csv_col for csv_col, mapped_col in bank.header_map.items() 
                    if mapped_col == "Date"), None)
    amount_cols = [csv_col for csv_col, mapped_col in bank.header_map.items() 
                  if mapped_col == "Amount"]
    desc_cols = [csv_col for csv_col, mapped_col in bank.header_map.items() 
                if mapped_col in ["Description", "Reference"]]
    
    if not date_col:
        raise ValueError(f"No Date column mapped in {bank.name}'s header_map")
    if not amount_cols:
        raise ValueError(f"No Amount column mapped in {bank.name}'s header_map")
    if not desc_cols:
        raise ValueError(f"No Description/Reference column mapped in {bank.name}'s header_map")
    
    # Check minimum rows
    if len(df) < 5:
        raise ValueError(f"CSV file has only {len(df)} rows. Minimum required: 5 rows")
    
    # Check for missing values in required columns
    missing_dates = df[date_col].isna().sum()
    if missing_dates > 0:
        raise ValueError(f"Found {missing_dates} rows with missing dates in column '{date_col}'")
    
    # For description, check if at least one description column has a value
    if all(df[desc_col].isna().all() for desc_col in desc_cols):
        raise ValueError(f"All rows are missing descriptions in columns {desc_cols}")


def print_csv_info(df, bank_name):
    """
    Displays general information about the DataFrame, such as number of columns and rows.
    """
    print("")
    print(f"{bank_name} CSV Information:")
    print(f"\tColumns x rows: {df.shape[1]} x {df.shape[0]}")
    print("\tColumn names:", list(df.columns))
    print("")

def _compare_headers(df, bank):
    """
    Compares DataFrame column headers with bank's header_map.
    Returns a tuple of two lists:
    - Unmatched CSV headers (headers in DataFrame but not in header_map)
    - Unused header_map keys (keys in header_map but not in DataFrame)
    
    Args:
        df (pd.DataFrame): DataFrame containing the CSV data
        bank (Bank): Bank instance containing the header_map
    """
    csv_headers = set(header.strip().lower() for header in df.columns)
    map_headers = set(header.strip().lower() for header in bank.header_map.keys())
    
    # Find headers that exist in CSV but not in header_map
    unmatched_csv = [header for header in df.columns 
                     if header.strip().lower() not in map_headers]
    
    # Find headers that exist in header_map but not in CSV
    unused_map = [header for header in bank.header_map.keys() 
                  if header.strip().lower() not in csv_headers]
    
    # Print results 
    if unmatched_csv:
        print(f"Warning! Unmatched CSV headers: {unmatched_csv}. These headers are in the CSV but not in the bank's header map. They will be ignored.")
    else:
        print(f"All CSV headers match the bank's header map.")
    # if unused_map:
    #     print(f"Unused header map keys for {bank.name}: {unused_map}")
    # else:
    #     print(f"All header map keys are used in the CSV for {bank.name}.")
        
    return unmatched_csv, unused_map


def create_unified_dataframe(df, bank):
    """
    Creates a unified DataFrame with standardized headers from a bank-specific DataFrame.
    
    Args:
        df (pd.DataFrame): Source DataFrame with bank-specific headers
        bank (Bank): Bank instance containing header mapping rules
        
    Returns:
        pd.DataFrame: New DataFrame with unified headers
    """
    # Create empty DataFrame with unified headers
    unified_df = pd.DataFrame(columns=list(udb.ubd.unified_headers.keys()))
    
    # Create reverse mapping (unified header -> list of bank headers)
    reverse_map = {}
    for bank_header, unified_header in bank.header_map.items():
        if unified_header not in reverse_map:
            reverse_map[unified_header] = []
        reverse_map[unified_header].append(bank_header)
    
    # Process each unified header
    for unified_header, data_type in udb.ubd.unified_headers.items():
        if unified_header == "Bank":
            # Fill bank name for all rows
            unified_df["Bank"] = bank.name
            continue
            
        if unified_header == "Unused":
            continue
            
        if unified_header not in reverse_map:
            print(f"Warning: No mapping found for unified header '{unified_header}'")
            continue
            
        bank_columns = reverse_map[unified_header]
        
        if data_type in ["currency", "YYYY-MM-DD"]:
            # For Date, Amount, Balance: check for conflicts
            non_empty_cols = [col for col in bank_columns if not df[col].isna().all()]
            
            if len(non_empty_cols) == 0:
                continue
            elif len(non_empty_cols) == 1:
                unified_df[unified_header] = df[non_empty_cols[0]]
            else:
                # Check if all columns have the same values where not null
                first_col = non_empty_cols[0]
                for other_col in non_empty_cols[1:]:
                    mask = ~df[first_col].isna() & ~df[other_col].isna()
                    if not (df.loc[mask, first_col] == df.loc[mask, other_col]).all():
                        raise ValueError(f"Conflicting values found in {unified_header} columns: {non_empty_cols}")
                
                # Combine columns, taking first non-null value for each row
                unified_df[unified_header] = df[non_empty_cols].bfill(axis=1).iloc[:, 0]
                
        elif data_type == "string":
            # For string types: concatenate non-empty values with warning
            if len(bank_columns) > 1:
                print(f"Warning: Multiple columns mapped to {unified_header}: {bank_columns}")
                
            # Combine all non-null values with ' | ' separator
            combined = df[bank_columns].apply(
                lambda row: ' | '.join(str(val) for val in row.dropna() if str(val).strip()), 
                axis=1
            )
            unified_df[unified_header] = combined
    
    return unified_df


#========= Deprecated functions =========

def validate_csv_headers(csv_path, bank_instance):
    """
    Validates that all headers in the CSV file match exactly one entry in the bank's header_map.
    Raises ValueError if a header is missing or if there are duplicates.
    """
    import pandas as pd

    # Read only the header row
    df = pd.read_csv(csv_path, delimiter=bank_instance.cvs_delimiter, encoding=bank_instance.csv_encoding, nrows=0)
    csv_headers = list(df.columns)

    # Get the header_map from the bank instance
    header_map = bank_instance.header_map

    # Reverse the mapping for quick lookup
    mapped_headers = set(header_map.keys())

    unmatched_headers = []
    duplicate_matches = []

    for header in csv_headers:
        # Count matches in header_map (should be exactly 1)
        matches = [k for k in mapped_headers if k.strip().lower() == header.strip().lower()]
        if len(matches) == 0:
            unmatched_headers.append(header)
        elif len(matches) > 1:
            duplicate_matches.append(header)

    if unmatched_headers:
        raise ValueError(f"CSV header(s) not found in {bank_instance.name} header_map: {unmatched_headers}")
    if duplicate_matches:
        raise ValueError(f"CSV header(s) have multiple matches in {bank_instance.name} header_map: {duplicate_matches}")

    print(f"All CSV headers for {bank_instance.name} are valid and uniquely mapped.")

# Example usage:
# validate_csv_headers(csv_path, bank)

def _detect_start_transaction_table(df):
    """
    Detects the row index where the actual transaction table starts in a DataFrame loaded from a CSV file.
    Returns the index of the header row (the row with the most non-empty columns).
    """
    max_non_empty = 0
    header_row_idx = 0
    for idx, row in df.iterrows():
        non_empty = row.count()
        if non_empty > max_non_empty:
            max_non_empty = non_empty
            header_row_idx = idx
    if header_row_idx > 0:
        print("Note: detected starting table at row ", header_row_idx)
    return header_row_idx

def _extract_transaction_table(df):
    """
    Given a DataFrame loaded from a CSV with possible extra info rows at the top and bottom,
    detects and returns only the actual transaction table as a new DataFrame.
    Assumes the transaction table header is the row with the most non-empty columns,
    and the table ends before a row with much fewer non-empty columns (like a balance row).
    """
    df_transactions = df.copy()  # Work on a copy to avoid modifying the original DataFrame
    # Find the header row (most non-empty columns)
    max_non_empty = 0
    header_row_idx = 0
    for idx, row in df.iterrows():
        non_empty = row.count()
        if non_empty > max_non_empty:
            max_non_empty = non_empty
            header_row_idx = idx
            if non_empty == len(df.columns):
                # If we find a row with all columns filled, we assume it's the header
                break
    if header_row_idx > 0:
        print(f"Detected csv header row at index {header_row_idx}")
        df_transactions = df.iloc[header_row_idx:]
        
    # Remove rows at the bottom that are not transactions (e.g., balance rows)
    # Detect if the last row has only 4 non-empty cells
    if not df_transactions.empty and df_transactions.iloc[-1].count() == 4:
        df_transactions = df_transactions.iloc[:-1]  # Remove the last row
        df_transactions.reset_index(drop=True, inplace=True)  # Reset index after slicing
        
    return df_transactions
    # TODO find the balance before and after that's in the DB csv to add another check. Might require DB class? it's quite specific to DB

def _match_header(column_name, header_categories_list):
    """
    Compares a column name to the possible header names in header_list.
    Returns a list of all matched header categories (can be empty if no match is found).
    Matching is case-insensitive and checks if the header_list string is contained in the column name.
    """
    column_name_lower = column_name.lower()
    matches = []
    for header_category in header_categories_list:
        for category, possible_names in header_category.items():
            for possible_name in possible_names:
                if possible_name.lower() in column_name_lower:
                    matches.append(category)
                    break  # Only add the category once per header_category
    return matches




