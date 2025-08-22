import logging as log
from datetime import datetime
import os

# Configure logging once at application startup
def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure file handler with timestamp in filename
    log_file = os.path.join(log_dir, f"accounting_{datetime.now():%Y%m%d_%H%M%S}.log")
    
    log.basicConfig(
        level=log.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            log.FileHandler(log_file),
            log.StreamHandler()  # Also output to console
        ]
    )

# Use in your code
logger = log.getLogger(__name__)

def process_bank_csv(bank, csv_path):
    logger.info(f"Processing CSV for bank: {bank.name}")
    try:
        # ...existing code...
        logger.debug(f"Found {len(df)} transactions")
    except Exception as e:
        logger.error(f"Failed to process CSV: {e}", exc_info=True)
        raise