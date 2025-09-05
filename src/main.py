import os
import pandas as pd
import yaml_config as yaml_config
import csv_processor as csv_processor
import banks_format as banks_format
import unified_format as udb
from utils.utils import log, setup_logging, print_processing_summary

# TODO: in DB, read top rows of the CSV file and read the starting balance
# TODO: add checks for every error!
# - In the load transaction table, all entries should have a date, a description and an amount
# - CSV tables should have at least x rows (at least 1 or 2?)

# Initialize logging
setup_logging()

# Load base_path from local_settings.yaml
local_settings = yaml_config.load_local_settings()
banks_base_path = local_settings["banks_base_path"]
log.info("\n" + f"Using banks base path: {banks_base_path}")

# Load CSV file for each bank
csv_results = {}
for bank_cls in banks_format.Bank.__subclasses__():
    try:
        bank = bank_cls()  # instantiate the bank
        log.info("\n" + f"Processing bank: {bank.name}")
        log.info("="*30)
                
        df = csv_processor.load_csv_file(os.path.join(banks_base_path, bank.name, bank.csv_filename), bank)
        
        csv_results[bank.name] = True
        
    except ValueError as e:
        # Extract only the error message without the traceback
        log.error(f"Error processing bank {bank_cls.__name__}: {str(e)}")
        csv_results[bank_cls.__name__] = False
        continue
      
    # Create unified DataFrame
    #unified_df = csv_processor.create_unified_dataframe(df, bank)
    #log.info("\nUnified DataFrame Info:")
    #csv_processor.print_csv_info(unified_df, f"{bank} (Unified)")


# Print summary of processing results
print_processing_summary(csv_results)

