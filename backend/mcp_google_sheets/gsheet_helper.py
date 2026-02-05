import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# Get absolute path to this file's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_sheet(sheet_name: str, worksheet_name="Sheet1"):
    """
    Connect to Google Sheet and return worksheet object
    """
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds_path = os.path.join(BASE_DIR, "credentials.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    try:
        sheet = client.open(sheet_name).worksheet(worksheet_name)
    except gspread.SpreadsheetNotFound:
        raise Exception(f"Spreadsheet '{sheet_name}' not found or not shared with service account.")
    except gspread.WorksheetNotFound:
        raise Exception(f"Worksheet '{worksheet_name}' not found in spreadsheet '{sheet_name}'.")
    return sheet

def add_registration(name: str, phone: str, email: str, course: str):
    """
    Append a new row with user registration details
    """
    try:
        sheet = get_sheet("UserRegistrations")  # <-- Make sure this matches your Sheet title
        sheet.append_row([name, phone, email, course])
        return True
    except Exception as e:
        # Print full exception for debugging
        print("Google Sheets error:", e)
        raise e
