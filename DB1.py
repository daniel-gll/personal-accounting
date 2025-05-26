# Functions to process CSV files with the bank transactions
import pandas as pd

def load_csv_file(csv_path, bank_name):
    
    """
    Loads a CSV file with specified encodings.
    Args:
        csv_path (str): Path to the CSV file.
        bank_name (str): Name of the bank for logging purposes.
    Returns:
        pd.DataFrame: Loaded DataFrame from the CSV file.
    """
    print(f"Loading CSV file for {bank_name} at {csv_path}")
    
    encodings_to_try = ["utf-8", "cp1252", "ISO-8859-1"]

    for enc in encodings_to_try:
        try:
            df = pd.read_csv(csv_path, delimiter=';', encoding=enc)
            break
        except UnicodeDecodeError:
            print(f"Failed to load with encoding: {enc}")
    else:
        raise UnicodeDecodeError(f"Could not decode {csv_path} with tried encodings: {encodings_to_try}")
    
    print(f"Successfully loaded CSV file with encoding: {enc}")
    return df


def print_csv_info(df, bank_name):
    """
    Displays general information about the DataFrame, such as number of columns and rows.
    """
    print("")
    print(f"{bank_name} CSV Information:")
    print(f"\tColumns x rows: {df.shape[1]} x {df.shape[0]}")
    print("\tColumn names:", list(df.columns))
    print("")

def detect_start_transaction_table(df):
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

def extract_transaction_table(df):
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


# TODO make this function only internal, not public
def match_header(column_name, header_categories_list):
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

# Example usage:
# matched = match_header(df.columns[i], header_list)
# print(f"Column '{df.columns[i]}' matched to headers: {matched}")

# TODO: if multiple header do not have a match, throw a warning. E.g ha pasado con DB
def match_headers(df, header_categories_list):
    """
    Iterates over all columns in the DataFrame and matches each header to the header categories.
    Returns a dictionary mapping column names to their matched categories.
    """
    matches = {}
    for col in df.columns:
        matched = match_header(col, header_categories_list)
        matches[col] = matched
    return matches



