from tkinter import *
import mysql.connector
import os

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Tecboy1122",
  database="inventorydb"
)

def login():
    login_id = login_id_entry.get()
    password = password_entry.get()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM login WHERE LoginID = %s AND Password = %s", (login_id, password))
    result = cursor.fetchone()

    if result:
        # Successful login, close the login window
        login_window.destroy()

        # Open the main window
        os.system("python FinalTrial.py")

    else:
        # Incorrect login information
        error_label.config(text="Invalid LoginID or Password")
        password_entry.delete(0, END)

# Create the login window
login_window = Tk()
login_window.title("Login")

# Set the size of the window and center it on the screen
window_width = 400
window_height = 300
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
login_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

# Create labels and entry fields for login information
login_id_label = Label(login_window, text="LoginID:", font=("Arial", 16))
login_id_label.grid(row=0, column=0, padx=10, pady=10)
login_id_entry = Entry(login_window, font=("Arial", 16))
login_id_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = Label(login_window, text="Password:", font=("Arial", 16))
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = Entry(login_window, show="*", font=("Arial", 16))
password_entry.grid(row=1, column=1, padx=10, pady=10)

login_icon = PhotoImage(file="login.png").subsample(6, 6)
login_button = Button(login_window, image=login_icon, command=login)
login_button.grid(row=2, columnspan=2, padx=10, pady=10)

error_label = Label(login_window, fg="red", font=("Arial", 12))
error_label.grid(row=3, columnspan=2, padx=10, pady=10)

# Run the main event loop
login_window.mainloop()
