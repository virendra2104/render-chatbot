from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "19Gdrjmvzsn1oV-DPlgUYoSuPcw7DL4IrlfgxHwf6qHA"
RANGE = "Sheet1!A:E"
CREDS_FILE = "backend/mcp_google_sheets/credentials.json"

# Authentication
creds = Credentials.from_service_account_file(
    CREDS_FILE,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

service = build("sheets", "v4", credentials=creds)

# Append test data
service.spreadsheets().values().append(
    spreadsheetId=SPREADSHEET_ID,
    range=RANGE,
    valueInputOption="RAW",
    body={"values": [["Test", "test@example.com", "1234567890", "Python Course"]]}
).execute()

print("Data added successfully!")
