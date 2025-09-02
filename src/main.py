import os #Can be removed?
import pandas as pd
import yaml_config as yaml_config
import csv_processor as csv_processor
import banks_format as banks_format
from utils.utils import log, setup_logging

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
results = {}
for bank_cls in banks_format.Bank.__subclasses__():
    bank_name = bank_cls.__name__
    try:
        bank = bank_cls()  # instantiate the bank
        bank_name = bank.name  # Update with proper name from instance
        log.info("\n" + f"Processing bank: {bank_name}")
        log.info("="*30)
        # Use os.path.join for better path handling across operating systems
        csv_path = os.path.join(banks_base_path, str(bank), bank.csv_filename)
                    
        df = csv_processor.load_csv_file(csv_path, bank)
        
        csv_processor.print_csv_info(df, bank_name)
        csv_processor.validate_csv_headers(df, bank)
        
        results[bank_name] = True
        
    except Exception as e:
        log.error(f"Error processing {bank_name}: {str(e)}")
        results[bank_name] = False
        continue  # Continue with next bank even if this one fails
    
    # Create unified DataFrame
    #unified_df = csv_processor.create_unified_dataframe(df, bank)
    #log.info("\nUnified DataFrame Info:")
    #csv_processor.print_csv_info(unified_df, f"{bank} (Unified)")

# Print summary of processing results
log.info("\n" + "="*50)
log.info("PROCESSING SUMMARY")
log.info("="*50)
successful = [name for name, success in results.items() if success]
failed = [name for name, success in results.items() if not success]

if successful:
    log.info(f"Successfully processed: {', '.join(successful)}")
if failed:
    log.error(f"Failed to process: {', '.join(failed)}")

log.info(f"Total: {len(results)} banks, {len(successful)} successful, {len(failed)} failed")

