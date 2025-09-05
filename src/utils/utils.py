import logging as log
from datetime import datetime
import os

# Add colorama for colored console output
try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Fallback: define dummy Fore and Style to avoid NameError
    class Dummy:
        RESET_ALL = ""
    class ForeDummy(Dummy):
        CYAN = ""
        GREEN = ""
        YELLOW = ""
        RED = ""
        MAGENTA = ""
        WHITE = ""
    Fore = ForeDummy()
    Style = Dummy()

class ColorFormatter(log.Formatter):
    LEVEL_COLORS = {
        log.DEBUG: Fore.CYAN,
        log.INFO: Fore.WHITE,
        log.WARNING: Fore.YELLOW,
        log.ERROR: Fore.RED,
        log.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, "")
        message = super().format(record)
        if COLORAMA_AVAILABLE and record.levelno in self.LEVEL_COLORS:
            return f"{color}{message}{Style.RESET_ALL}"
        return message

def setup_logging(show_time=False, show_logger=False, show_level=False, log_to_file=False):
    """
    Configure logging with optional display of time/date, logger name, and log level.
    Args:
        show_time (bool): Include timestamp in log output
        show_logger (bool): Include logger name in log output
        show_level (bool): Include log level in log output
        log_to_file (bool): Enable or disable logging to a file
    """
    # Build log format string
    format_parts = []
    if show_time:
        format_parts.append('%(asctime)s')
    if show_logger:
        format_parts.append('%(name)s')
    if show_level:
        format_parts.append('%(levelname)s')
    format_parts.append('%(message)s')
    log_format = ' - '.join(format_parts)

    # Initialize handlers list
    handlers = []

    # Add file handler if enabled
    if log_to_file:
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"accounting_{datetime.now():%Y%m%d_%H%M%S}.log")
        file_handler = log.FileHandler(log_file)
        file_handler.setFormatter(log.Formatter(log_format))
        handlers.append(file_handler)

    # Console handler (with color if available)
    stream_handler = log.StreamHandler()
    if COLORAMA_AVAILABLE:
        stream_handler.setFormatter(ColorFormatter(log_format))
    else:
        stream_handler.setFormatter(log.Formatter(log_format))
    handlers.append(stream_handler)

    log.basicConfig(
        level=log.INFO,
        handlers=handlers
    )
    
def print_processing_summary(results):
    """
    Print a summary of processing results for banks.
    
    Args:
        results (dict): Dictionary mapping bank names to True/False for success
    """
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
