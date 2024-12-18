import os

from datetime import datetime
import pytz

LOG_DIR = '/var/log/psychochauffeurbot'

# Add Kyiv timezone constant
KYIV_TZ = pytz.timezone('Europe/Kiev')

def get_daily_log_path_optimized(date=None, log_dir=LOG_DIR, timezone=KYIV_TZ):
    """Get the path to the daily log file for the specified date."""
    if date is None:
        # Use the current date in the specified timezone
        date = datetime.now(timezone)
    elif not isinstance(date, datetime):
        raise ValueError("The 'date' parameter must be a datetime object or None.")
    elif date.tzinfo is None:
        # If date has no timezone, assume it's in the specified timezone
        date = timezone.localize(date)
    
    log_path = os.path.join(
        log_dir, 
        f"chat_{date.strftime('%Y-%m-%d')}.log"
    )
    
    return log_path