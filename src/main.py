import pandas as pd
import yaml_config as yaml_config
import db1 as db1
import banks_format as banks_format

# TODO: in DB, read top rows of the CSV file and read the starting balance
# TODO: add checks for every error!
# - In the load transaction table, all entries should have a date, a description and an amount
# - CSV tables should have at least x rows (at least 1 or 2?)

#Load base_path from local_settings.yaml
local_settings = yaml_config.load_local_settings()
banks_base_path = local_settings["banks_base_path"]
print("")
print("")
print(f"Using banks base path: {banks_base_path}")

# Load CSV file
for bank_cls in banks_format.Bank.__subclasses__():
    
    bank = bank_cls()  # instantiate the bank
    print("")
    print("")
    print(f"Processing bank: {bank}")
    print("==========================")
    csv_path = f"{banks_base_path}\\{bank}\\{bank.csv_filename}"
    
    df = db1.load_csv_file(csv_path, bank)
    
    db1.print_csv_info(df, bank)
        
    # Create unified DataFrame
    unified_df = db1.create_unified_dataframe(df, bank)
    
    print("\nUnified DataFrame Info:")
    db1.print_csv_info(unified_df, f"{bank} (Unified)")
    
    