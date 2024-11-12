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
    
    def display_rooms(self):
        # Print the list of all rooms in the hotel
        print("Available rooms in the hotel:")
        for room in self.rooms:
            print(room)
    def display_available_rooms(self):
        # Find rooms that are not reserved
        available_rooms = [room for room in self.rooms if room not in self.reservations]
        
        # Print the list of available rooms
        if available_rooms:
            print("Available rooms:")
            for room in available_rooms:
                print(room)
        else:
            print("No rooms available")


    def make_reservation(self, name, room, check_in, check_out):
        # Check if the room is available
        if room in self.rooms and room not in self.reservations:
            # Add reservation details to the dictionary
            self.reservations[room] = {"name": name, "check_in": check_in, "check_out": check_out}
            
            # Add the reservation to the Google Sheet
            worksheet = SHEET.worksheet("rooms")
            worksheet.append_row([name, room, str(check_in), str(check_out)])
            
            print(f"Room {room} reserved for {name} from {check_in} to {check_out}")
        else:
            print(f"Room {room} is not available")
        
        # Refresh reservations from the sheet
        self.get_reservations_from_sheet()
