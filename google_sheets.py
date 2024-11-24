from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def connect_google_sheets(credentials_json):
    credentials = Credentials.from_authorized_user_info(credentials_json)
    service = build('sheets', 'v4', credentials=credentials)
    # Example: Get data from a specific sheet
    sheet_id = "<YOUR_SHEET_ID>"
    range_name = "Sheet1!A1:Z1000"
    result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_name).execute()
    return result.get('values', [])
