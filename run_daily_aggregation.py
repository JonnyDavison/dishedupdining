import logging
import time
import subprocess
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def run_command():
    logging.info("Running daily aggregation command")
    result = subprocess.run(["python", "manage.py", "aggregate_daily_data"], capture_output=True, text=True)
    if result.returncode == 0:
        logging.info("Aggregation completed successfully")
    else:
        logging.error(f"Aggregation failed: {result.stderr}")

while True:
    now = datetime.now()
    if now.hour == 1 and now.minute == 0:
        run_command()
    time.sleep(60)