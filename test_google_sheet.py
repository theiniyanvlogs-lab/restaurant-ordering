import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

print("✅ Connected to Google Sheets")

sheet = client.open("RestaurantDB").worksheet("Menu")

print("✅ Opened Menu sheet")

records = sheet.get_all_records()

print(f"Total Records: {len(records)}")

for row in records:
    print(row)
