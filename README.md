# KekaTimecardFiller

Automate filling your Keka timecard for a given month using the official API. This tool is intended for use only with explicit manager approval and when you are unable to fill timecards daily.

## Features
- Automatically fills attendance for all working days in a month
- Skips weekends and holidays
- Logs status for each day and provides a summary
- Reads configuration from a `.env` file

## How to Use
1. **Clone the repository** and navigate to the project folder.
2. **Create a Python virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure your `.env` file** (see `.env.sample` for template):
   - `KEKA_BEARER_TOKEN`: Your Keka API Bearer token
   - `KEKA_EMPLOYEE_ID`: Your employee ID
   - `KEKA_HOLIDAYS`: Comma-separated list of holidays (YYYY-MM-DD)
   - `KEKA_MONTH`: Month number (e.g., 2 for February)
   - `KEKA_YEAR`: Year (e.g., 2026)
5. **Run the script**:
   ```bash
   python fill_timecard.py
   ```

## When to Use
- Only use this tool if you are too busy to fill timecards daily.
- Use strictly with your manager's approval for synthetic timecard entries.
- Do not use for fraudulent or unauthorized attendance regularization.

## Disclaimer
This tool is provided for convenience and should only be used with explicit permission from your manager. Unauthorized or inappropriate use may violate company policy and could result in disciplinary action. The author is not responsible for any misuse.

---

For questions or issues, please open an issue in the repository.
