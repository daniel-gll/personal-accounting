import pandas as pd
import yaml_config as yaml_config
import db1 as db1

# TODO: create a class??
# TODO: in DB, read top rows of the CSV file and read the starting balance
# TODO: add checks!
# - In the load transaction table, all entries should have a date, a description and an amount
# - CSV tables should have at least x rows (at least 1 or 2?)

#Load base_path from local_settings.yaml
local_settings = yaml_config.load_local_settings()
banks_base_path = local_settings["banks_base_path"]
banks_csv_filename = local_settings["banks_csv_filename"]

#Load bank configuration
bank_config = yaml_config.load_config()
banks_list = bank_config["Banks"]
header_categories_list = bank_config["Headers"]

# Load CSV file
for bank_entry in banks_list:
    
    bank_name = list(bank_entry.keys())[0]  # e.g., "Abanca", "DB", "N26"
    print("")
    print(f"Processing bank: {bank_name}")
    print("==============================")
    csv_path = f"{banks_base_path}\\{bank_name}\\{banks_csv_filename}"
    
    df = db1.load_csv_file(csv_path, bank_name)
    df = db1.extract_transaction_table(df)
        
    db1.print_csv_info(df, bank_name)

    all_matches = db1.match_headers(df, header_categories_list)
    print("Header matches found:")
    for col, matched in all_matches.items():
        print(f"\t{col:<20}\t->\t{matched}")
        

    