import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('hotel-management')

# Define the HotelManagement class
class HotelManagement:
    def __init__(self):
        # Initialize rooms in the hotel (20 rooms total)
        self.rooms = [f"Room {i}" for i in range(1, 21)]
        
        # Initialize an empty dictionary for reservations
        self.reservations = {}

        # Load existing reservations from the Google Sheet
        self.get_reservations_from_sheet()

    def get_reservations_from_sheet(self):
        # Access the worksheet named "rooms"
        worksheet = SHEET.worksheet("rooms")
        

        # Fetch all records from the worksheet
        records = worksheet.get_all_records()
        
        # Map reservations into a structured dictionary
        self.reservations = {
            record["Room"].replace(" ", ""): {
                "name": record["Name"].strip(),
                "check_in": record["Check-in "].strip(),
                "check_out": record["Check-out"].strip()
            }
            for record in records if record["Name"]
        }
    
