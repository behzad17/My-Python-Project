import gspread
from google.oauth2.service_account import Credentials
import datetime


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

        # Initialize rooms in the hotel (5 rooms total)
        self.rooms = [f"Room{i}" for i in range(1, 6)]

        # Initialize an empty dictionary for reservations
        self.reservations = {}

        # Checked_out rooms list
        self.checked_out_rooms = []

        # Load existing reservations from the Google Sheet
        self.get_reservations_from_sheet()

    def get_reservations_from_sheet(self):
        """
        Load reservations from Google Sheet
        """
        worksheet = SHEET.worksheet("rooms")
        records = worksheet.get_all_records()

        # Reset reservations dictionary
        self.reservations = {}

        for record in records:
            
            room = str(record["Room"]).strip()  
            name = str(record["Name"]).strip()
            check_in = str(record["Check-in"]).strip()
            check_out = str(record["Check-out"]).strip()

          
            if room and name and check_in and check_out:
                if room not in self.reservations:
                    self.reservations[room] = [] 
                self.reservations[room].append({
                    "name": name,
                    "check_in": check_in,
                    "check_out": check_out
                })


    def display_reserved_rooms(self):
        """
        Print the list of reserved rooms in the hotel
        """
        print("Reserved rooms:")
        if self.reservations:
            for room, reservations in self.reservations.items():
                    print(f"\n{room}:")
                    for res in reservations:
                        print(f" Guest {res['name']} from {res['check_in']} to {res['check_out']}")

        else:
            print("No rooms are currently reserved.")

    def display_available_rooms(self):
        # Find rooms that are not reserved

        available_rooms = [
            room for room in self.rooms if room not in self.reservations]
        # Print the list of available rooms
        print("Available rooms:")
        if available_rooms:
            for room in available_rooms:
                print(room)

        else:
            print("No rooms available.")

    def display_checked_out_rooms(self):
        """
        Show checked-out rooms
        """
        print("checked-out rooms:")
        if self.checked_out_rooms:
            for room in self.checked_out_rooms:
                print(room)
        else:
            print("No rooms have been checked out.")


    def make_reservation(self, name, room, check_in, check_out):
        """
        Make a reservation for a guest
        """
    
        if room in self.reservations:
            for res in self.reservations[room]:
                if check_in <= res["check_out"] and check_out >= res["check_in"]:
                    print(f"❌ Room {room} is already reserved from {res['check_in']} to {res['check_out']}.")
                    return

        # add new reservation
        if room not in self.reservations:
            self.reservations[room] = []

        self.reservations[room].append({
            "name": name,
            "check_in": check_in,
            "check_out": check_out
        })

        print(f"✅ Room {room} is now reserved for {name} from {check_in} to {check_out}.")

   
        try:
            worksheet = SHEET.worksheet("rooms")
            worksheet.append_row([room, name, check_in, check_out])
            self.get_reservations_from_sheet()
        except Exception as e:
            print(f"❌ Error updating Google Sheet: {e}")


    def check_out_guest(self, room):
        """
        Check out a guest and update the list.
        """
        room = room.strip()

     
        if room in self.reservations:
            try:
                worksheet = SHEET.worksheet("rooms")
                records = worksheet.get_all_records()

               
                print(f"\n📌 Room {room} has the following reservations:")
                for i, res in enumerate(self.reservations[room], start=1):
                    print(f"{i}. Guest {res['name']} from {res['check_in']} to {res['check_out']}")

                choice = int(input("\nEnter the number of the guest to check out: "))
                if 1 <= choice <= len(self.reservations[room]):
                    removed_guest = self.reservations[room].pop(choice - 1)  
                
                  
                    update_records = [record for record in records if not (
                        str(record["Room"]).strip() == room.strip() and 
                        str(record["Name"]).strip() == removed_guest["name"] and
                        str(record["Check-in"]).strip() == removed_guest["check_in"] and
                        str(record["Check-out"]).strip() == removed_guest["check_out"]
                    )]

                   
                    worksheet.clear()
                    worksheet.append_row(["Room", "Name", "Check-in", "Check-out"])
                    for record in update_records:
                        worksheet.append_row([record["Room"], record["Name"], record["Check-in"], record["Check-out"]])

                    print(f"✅ Guest {removed_guest['name']} checked out from Room {room}.")

                  
                    if not self.reservations[room]:  
                        del self.reservations[room]
                        self.checked_out_rooms.append(room) 
                
                    self.get_reservations_from_sheet()

                else:
                    print("❌ Invalid choice.")

            except Exception as e:
                print(f"❌ Error updating Google Sheet: {e}")

        else:
            print(f"Room {room} is not currently reserved.")


# running the code
if __name__ == "__main__":
    hotel = HotelManagement()

    while True:

        print("\n--- Hotel Management System ---")
        print("1. Reserved rooms")
        print("2. Available rooms")
        print("3. Checked-out rooms")
        print("4. New reservation")
        print("5. Check out")
        print("6. Exit")

        # get the user`s choice
        choice = input("Enter your choice: ")

        if choice == "1":
            hotel.display_reserved_rooms()
        elif choice == "2":
            hotel.display_available_rooms()
        elif choice == "3":
            hotel.display_checked_out_rooms()
        elif choice == "4":
            # Collect reservation details from user
            name = input("Enter guest's name: ")
            valid_rooms = [f"Room{i}" for i in range(1, 6)]
            room = input("Enter room number (e.g., Room3): ").strip()

            while room not in valid_rooms:
                print("❌ Invalid room number. Please enter a valid room (Room1 - Room5).")
                room = input("Enter room number (e.g., Room3): ").strip()

            check_in = input("Enter check-in date (YYYY-MM-DD): ").strip()
            check_out = input("Enter check-out date (YYYY-MM-DD): ").strip()

            hotel.make_reservation(name, room, check_in, check_out)


        elif choice == "5":
            room = input("Enter room number to check out (e.g., Room3): ")
            hotel.check_out_guest(room)
        elif choice == "6":
            print("Exit")
            break
        else:
            print("Invalid choice. Try again.")
