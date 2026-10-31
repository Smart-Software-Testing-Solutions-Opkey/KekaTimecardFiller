import os
import random
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

API_URL = "https://ssts.keka.com/k/attendance/api/mytime/attendance/saveattendanceadjustment"
AUTH_TOKEN = os.getenv("KEKA_BEARER_TOKEN")
EMPLOYEE_ID = int(os.getenv("KEKA_EMPLOYEE_ID"))
HOLIDAYS = [h.strip() for h in os.getenv("KEKA_HOLIDAYS", "").split(",") if h.strip()]  # Clean empty strings
MONTH = int(os.getenv("KEKA_MONTH"))
YEAR = int(os.getenv("KEKA_YEAR"))

HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

def is_weekend(date):
    # 5 = Saturday, 6 = Sunday
    return date.weekday() == 5 or date.weekday() == 6

def is_holiday(date):
    return date.strftime("%Y-%m-%d") in HOLIDAYS

def fill_timecard():
    start_date = datetime(YEAR, MONTH, 1)
    if MONTH == 12:
        end_date = datetime(YEAR + 1, 1, 1)
    else:
        end_date = datetime(YEAR, MONTH + 1, 1)
    current_date = start_date
    status_summary = {}
    while current_date < end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        if is_weekend(current_date):
            logging.info(f"{date_str}: Skipped (Weekend)")
            status_summary[date_str] = "Skipped (Weekend)"
        elif is_holiday(current_date):
            logging.info(f"{date_str}: Skipped (Holiday)")
            status_summary[date_str] = "Skipped (Holiday)"
        else:
            clock_in = current_date.replace(hour=9)
            clock_out = clock_in + timedelta(minutes=random.randint(9 * 60, 10 * 60))  # Random 9-10 hour workday
            clock_in_str = clock_in.strftime("%Y-%m-%dT%H:%M:00.000Z")
            clock_out_str = clock_out.strftime("%Y-%m-%dT%H:%M:00.000Z")
            payload = {
                "employeeId": EMPLOYEE_ID,
                "requestType": 1,
                "requestDate": date_str,
                "note": "Regularizing Attendance",
                "timeEntries": [
                    {
                        "actualTimestamp": clock_in_str,
                        "adjustedTimestamp": clock_in_str,
                        "timestamp": clock_in_str,
                        "originalPunchStatus": 0,
                        "modifiedPunchStatus": 0,
                        "punchStatus": 0,
                        "attendanceLogSource": 1,
                        "premiseName": "Attendance Adjustment",
                        "manualClockinType": 2,
                        "isAdjusted": True,
                        "isManuallyAdded": True,
                        "isEditable": True
                    },
                    {
                        "actualTimestamp": clock_out_str,
                        "adjustedTimestamp": clock_out_str,
                        "timestamp": clock_out_str,
                        "originalPunchStatus": 1,
                        "modifiedPunchStatus": 1,
                        "punchStatus": 1,
                        "attendanceLogSource": 1,
                        "premiseName": "Attendance Adjustment",
                        "manualClockinType": 2,
                        "isAdjusted": True,
                        "isManuallyAdded": True,
                        "isEditable": True
                    }
                ]
            }
            try:
                response = requests.post(API_URL, json=payload, headers=HEADERS)
                if response.status_code == 200:
                    logging.info(f"{date_str}: Success ({clock_in:%H:%M}-{clock_out:%H:%M})")
                    status_summary[date_str] = f"Success ({clock_in:%H:%M}-{clock_out:%H:%M})"
                else:
                    logging.error(f"{date_str}: Failed ({response.status_code}) {response.text}")
                    status_summary[date_str] = f"Failed ({response.status_code})"
            except Exception as e:
                logging.error(f"{date_str}: Exception {str(e)}")
                status_summary[date_str] = f"Exception: {str(e)}"
        current_date += timedelta(days=1)
    print("\nDay-wise Status Summary:")
    for day, status in status_summary.items():
        print(f"{day}: {status}")

if __name__ == "__main__":
    fill_timecard()
