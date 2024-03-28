# Glovo App

The Glovo Management System is a Python application designed to facilitate the management of clients, delivery agents (livreurs), and commands for a fictional delivery service. This application allows users to perform various tasks such as adding, removing, and viewing clients and delivery agents, as well as tracking commands assigned to them. It provides a user-friendly interface built with Tkinter, a Python GUI library, and utilizes SQLite3 for the backend database management. The application ensures efficient handling of delivery logistics by simplifying operations related to client management, agent assignment, and command tracking.


## Features

- **Manage Clients**: Add, remove, and view clients along with their address and number of commands.
- **Manage Livreurs**: Add, remove, and view delivery agents along with their number of commands and active status.
- **Manage Commands**: Add, remove, and view commands assigned to clients and livreurs.


## Developer Notes:

- **Login Functionality**: The code includes a basic login functionality with a hardcoded username and password ("admin").
- **User Interface**: Developers can customize the user interface layout and design by modifying the Tkinter widgets and their configurations.
- **Database Interaction**: Ensure proper handling of database interactions, including error checking and data validation to maintain data integrity.
- **Security Considerations**: For production use, implement secure authentication mechanisms and consider encrypting sensitive data stored in the database.



## Screenshots

![Screenshot](screenshot1.png)


![Screenshot](screenshot2.png)


![Screenshot](screenshot3.png)


## How to Run

1. Clone this repository to your local machine.
2. Make sure you have Python installed.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Run the application by executing `python glovo_app.py` in your terminal.

## Dependencies

- Python 3.x
- Tkinter
- SQLite3

## Contributing


Contributions are welcome! Please feel free to submit issues or pull requests.
