
# Hotel Management System

this is a Python project to manage hotel room reservation for a little hotel with 5 rooms. In the project i use **Google Sheets** to update data such as reservation , available rooms and check-in/outs.
The program has a menu to user also.

## Features

1. **Reserved Rooms**: To see which rooms have been reserved.
2. **Available rooms** To see which rooms are free to bookning.
3. **Checked-Out rooms** To see rooms that have been checked out.
4. **New reservation** To do a reservation by guest.
5. **Check out a gyest** Remove a reservation when guest leaves.

### How the code works

**Local Data Management** 
- The program keeps room reservation in a list inside the code and this list updates automatically when i add a new reservation or checked out a guest.

**Google Sheets Conection**
- When the program connects to a Google Sheet, any changes are saved in the google sheet.


## Requirements

1. **google-auth==2.36.0**
2. **google-auth-oauthlib==1.2.1**
3. **gspread==6.1.4**

## Google Sheet
I use a google sheet named hotel-management and worksheet named "rooms"


## link to deploy
You can find the deployed link of program on **Heroku** here: [Heroku](https://my-python-project-33005f6b5ac8.herokuapp.com/)
## link to GitHub repository
You can find the depository link on **GitHub** here: [GitHub](https://github.com/behzad17/My-Python-Project)