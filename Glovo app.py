import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect('glovo.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS clients
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, address TEXT, num_commands INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS livreurs
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, number_of_commands INTEGER, active_status TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS commands
             (id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT, livreur_id INTEGER, client_id INTEGER, command_date DATE, command_time TIME)''')
conn.commit()

selected_client_id = None  # Initialize selected_client_id variable

def refresh_clients_table():
    for row in clients_tree.get_children():
        clients_tree.delete(row)
    c.execute('''SELECT clients.id, clients.name, clients.address, COALESCE(cmd_counts.num_commands, 0) as num_commands
              FROM clients LEFT JOIN (SELECT client_id, COUNT(*) as num_commands FROM commands GROUP BY client_id) AS cmd_counts
              ON clients.id = cmd_counts.client_id''')
    for row in c.fetchall():
        clients_tree.insert("", tk.END, values=row)

def add_client():
    try:
        c.execute('INSERT INTO clients (name, address, num_commands) VALUES (?, ?, ?)',
                  (name_var.get(), address_var.get(), 0))
        conn.commit()
        refresh_clients_table()
        refresh_clients_dropdown()  
        name_var.set('')
        address_var.set('')
        messagebox.showinfo("Success", "Client added successfully.")
    except Exception as e:
        messagebox.showerror("Error", "Failed to add client. Error: " + str(e))

def remove_client():
    selected_item = clients_tree.selection()[0]
    client_id = clients_tree.item(selected_item)['values'][0]
    c.execute('DELETE FROM clients WHERE id = ?', (client_id,))
    conn.commit()
    refresh_clients_table()
    messagebox.showinfo("Success", "Client removed successfully.")

def show_main_menu():
    refresh_clients_table()
    notebook.select(0)

def refresh_livreurs_table():
    for row in livreurs_tree.get_children():
        livreurs_tree.delete(row)
    c.execute('SELECT *, (SELECT COUNT(*) FROM commands WHERE commands.livreur_id = livreurs.id) as num_commands FROM livreurs')
    for row in c.fetchall():
        livreurs_tree.insert("", tk.END, values=row)

def add_livreur():
    try:
        c.execute('INSERT INTO livreurs (name, number_of_commands, active_status) VALUES (?, ?, ?)',
                  (livreur_name_var.get(), 0, livreur_active_var.get()))
        conn.commit()
        refresh_livreurs_table()
        messagebox.showinfo("Success", "Livreur added successfully.")
    except Exception as e:
        messagebox.showerror("Error", "Failed to add livreur. Error: " + str(e))

def remove_livreur():
    selected_item = livreurs_tree.selection()[0]
    livreur_id = livreurs_tree.item(selected_item)['values'][0]
    c.execute('DELETE FROM livreurs WHERE id = ?', (livreur_id,))
    conn.commit()
    refresh_livreurs_table()
    messagebox.showinfo("Success", "Livreur removed successfully.")

def refresh_commands_table():
    for row in commands_tree.get_children():
        commands_tree.delete(row)
    c.execute('SELECT * FROM commands')
    for row in c.fetchall():
        commands_tree.insert("", tk.END, values=row)

def remove_command():
    selected_item = commands_tree.selection()[0]
    command_id = commands_tree.item(selected_item)['values'][0]
    c.execute('DELETE FROM commands WHERE id = ?', (command_id,))
    conn.commit()
    refresh_commands_table()
    messagebox.showinfo("Success", "Command removed successfully.")
def add_command():
    try:
        if selected_client_id is not None:  # Ensure a client is selected
            # Get the livreur with fewer than two commands
            c.execute('SELECT id, name FROM livreurs WHERE active_status="Active" AND number_of_commands < 2')
            livreur_data = c.fetchone()
            if livreur_data:
                livreur_id, livreur_name = livreur_data
                c.execute('INSERT INTO commands (product_name, livreur_id, client_id, command_date, command_time) VALUES (?, ?, ?, ?, ?)',
                          (product_name_var.get(), livreur_id, selected_client_id, date_var.get(), time_var.get()))
                # Update the number of commands for the livreur
                c.execute('UPDATE livreurs SET number_of_commands = number_of_commands + 1 WHERE id = ?', (livreur_id,))
                
                # Update the number of commands for the client
                c.execute('UPDATE clients SET num_commands = num_commands + 1 WHERE id = ?', (selected_client_id,))
                
                conn.commit()
                refresh_commands_table()
                refresh_clients_table()  # Refresh clients table to update the number of commands
                messagebox.showinfo("Success", f"Command transferred to the livreur: {livreur_name}")
            else:
                messagebox.showwarning("No Active Livreur", "There are no active livreurs available to handle the command.")
        else:
            messagebox.showwarning("No Client Selected", "Please select a client before adding a command.")
    except Exception as e:
        messagebox.showerror("Error", "Failed to register command. Error: " + str(e))

def select_client(event):
    global selected_client_id
    selected_client_name = clients_dropdown.get()
    if selected_client_name:  # If a client is selected
        # Fetch the client ID based on the selected client's name
        selected_client_id = c.execute('SELECT id FROM clients WHERE name = ?', (selected_client_name,)).fetchone()[0]

def select_livreur(event):
    global selected_livreur_id
    item = livreurs_tree.selection()[0]
    selected_livreur_id = livreurs_tree.item(item, 'values')[0]

def refresh_clients_dropdown():
    clients_dropdown['values'] = [row[1] for row in c.execute('SELECT id, name FROM clients')]



def refresh_data():
    refresh_clients_table()
    refresh_livreurs_table()

# GUI setup
root = tk.Tk()
root.title("Glovo App")

# Logo
logo_label = tk.Label(root, text="Glovo", font=("Arial", 24, "bold"))
logo_label.pack()

# Login Frame
login_frame = ttk.Frame(root)
login_frame.pack(pady=10)

tk.Label(login_frame, text="Username:").grid(row=0, column=0, sticky="e")
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1)

tk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky="e")
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1)

login_attempts = 0

def login():
    global login_attempts
    # Hardcoded username and password
    correct_username = "admin"
    correct_password = "admin"
    
    # Get the entered username and password
    entered_username = username_entry.get()
    entered_password = password_entry.get()
    
    # Check if the entered username and password are correct
    if entered_username == correct_username and entered_password == correct_password:
        messagebox.showinfo("Login Successful", "Welcome to Glovo App!")
        login_frame.destroy()
        create_management_interface()
    else:
        login_attempts += 1
        if login_attempts == 3:
            messagebox.showerror("Login Failed", "Maximum login attempts exceeded. Closing the application.")
            root.destroy()  # Close the application
        else:
            messagebox.showerror("Login Failed", f"Incorrect username or password. {3 - login_attempts} attempts remaining.")

login_button = ttk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, columnspan=2, pady=5)

def create_management_interface():
    global notebook, clients_frame, livreurs_frame, commands_frame
    global clients_tree, livreurs_tree, commands_tree, clients_dropdown
    global name_var, address_var, product_name_var, date_var, time_var, selected_livreur_id, selected_client_id, livreur_name_var, livreur_active_var

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    clients_frame = ttk.Frame(notebook)
    notebook.add(clients_frame, text="Manage Clients")

    livreurs_frame = ttk.Frame(notebook)
    notebook.add(livreurs_frame, text="Manage Livreurs")

    commands_frame = ttk.Frame(notebook)
    notebook.add(commands_frame, text="Manage Commands")

    # Manage Clients Interface
    tk.Label(clients_frame, text="Name").pack()
    name_var = tk.StringVar()
    name_entry = tk.Entry(clients_frame, textvariable=name_var)
    name_entry.pack()

    tk.Label(clients_frame, text="Address").pack()
    address_var = tk.StringVar()
    address_entry = tk.Entry(clients_frame, textvariable=address_var)
    address_entry.pack()

    add_client_button = tk.Button(clients_frame, text="Add Client", command=add_client)
    add_client_button.pack(pady=5)

    remove_client_button = tk.Button(clients_frame, text="Remove Client", command=remove_client)
    remove_client_button.pack(pady=5)

    main_menu_button = tk.Button(clients_frame, text="Main Menu", command=show_main_menu)
    main_menu_button.pack(pady=5)

    # Clients Table setup
    clients_tree = ttk.Treeview(clients_frame, columns=("ID", "Name", "Address", "Number of Commands"), show='headings')
    clients_tree.heading("ID", text="ID")
    clients_tree.heading("Name", text="Name")
    clients_tree.heading("Address", text="Address")
    clients_tree.heading("Number of Commands", text="Number of Commands")
    clients_tree.pack()

    refresh_clients_table()

    refresh_button = tk.Button(clients_frame, text="Refresh", command=refresh_data)
    refresh_button.pack(pady=5)

    # Manage Livreurs Interface
    tk.Label(livreurs_frame, text="Livreur Name").pack()
    livreur_name_var = tk.StringVar()
    livreur_name_entry = tk.Entry(livreurs_frame, textvariable=livreur_name_var)
    livreur_name_entry.pack()

    tk.Label(livreurs_frame, text="Active Status").pack()
    livreur_active_var = tk.StringVar()
    livreur_active_var.set("Active")  # Default to "Active"
    active_status_dropdown = ttk.Combobox(livreurs_frame, textvariable=livreur_active_var, values=["Active", "Inactive"])
    active_status_dropdown.pack()

    add_livreur_button = tk.Button(livreurs_frame, text="Add Livreur", command=add_livreur)
    add_livreur_button.pack(pady=5)

    remove_livreur_button = tk.Button(livreurs_frame, text="Remove Livreur", command=remove_livreur)
    remove_livreur_button.pack(pady=5)

    main_menu_livreur_button = tk.Button(livreurs_frame, text="Main Menu", command=show_main_menu)
    main_menu_livreur_button.pack(pady=5)

    livreurs_tree = ttk.Treeview(livreurs_frame, columns=("ID", "Name", "Number of Commands", "Active Status"), show='headings')
    livreurs_tree.heading("ID", text="ID")
    livreurs_tree.heading("Name", text="Name")
    livreurs_tree.heading("Number of Commands", text="Number of Commands")
    livreurs_tree.heading("Active Status", text="Active Status")
    livreurs_tree.pack()

    refresh_livreurs_table()

    refresh_button_livreur = tk.Button(livreurs_frame, text="Refresh", command=refresh_data)
    refresh_button_livreur.pack(pady=5)

    # Manage Commands Interface
    tk.Label(commands_frame, text="Product Name").pack()
    product_name_var = tk.StringVar()
    product_name_entry = tk.Entry(commands_frame, textvariable=product_name_var)
    product_name_entry.pack()

    tk.Label(commands_frame, text="Date").pack()
    date_var = tk.StringVar()
    date_entry = tk.Entry(commands_frame, textvariable=date_var)
    date_entry.pack()

    tk.Label(commands_frame, text="Time").pack()
    time_var = tk.StringVar()
    time_entry = tk.Entry(commands_frame, textvariable=time_var)
    time_entry.pack()

    tk.Label(commands_frame, text="Select Client").pack()
    clients_dropdown = ttk.Combobox(commands_frame)
    clients_dropdown.pack()
    refresh_clients_dropdown()

    add_command_button = tk.Button(commands_frame, text="Add Command", command=add_command)
    add_command_button.pack(pady=5)

    remove_command_button = tk.Button(commands_frame, text="Remove Command", command=remove_command)
    remove_command_button.pack(pady=5)

    main_menu_command_button = tk.Button(commands_frame, text="Main Menu", command=show_main_menu)
    main_menu_command_button.pack(pady=5)

    commands_tree = ttk.Treeview(commands_frame, columns=("ID", "Product Name", "Livreur ID", "Client ID", "Date", "Time"), show='headings')
    commands_tree.heading("ID", text="ID")
    commands_tree.heading("Product Name", text="Product Name")
    commands_tree.heading("Livreur ID", text="Livreur ID")
    commands_tree.heading("Client ID", text="Client ID")
    commands_tree.heading("Date", text="Date")
    commands_tree.heading("Time", text="Time")
    commands_tree.pack()

    refresh_commands_table()

    livreurs_tree.bind("<<TreeviewSelect>>", select_livreur)
    clients_dropdown.bind("<<ComboboxSelected>>", select_client)

root.mainloop()

# Close database connection on exit
conn.close()
