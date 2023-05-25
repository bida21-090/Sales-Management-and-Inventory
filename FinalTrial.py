import mysql.connector
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import Toplevel, Frame


"""

mydb = mysql.connector.connect(
    host="aws.connect.psdb.cloud",
    user="3s6pdi0iictqb3ybdex3",
    password="pscale_pw_JIjLc3UGpjx7AGWIReXKgH4oUZ2oHD9LRKXDpYFjlN",
    database="inventorydb",
    autocommit=True
)
"""
#16.	Implement SQL to store and retrieve the data.
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Tecboy1122",
  database="inventorydb"
)

# create a cursor object
mycursor = mydb.cursor()

# create a tkinter window
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("1250x700+50+25")
status_label = tk.Label(root, text="")
status_label.pack()



header = tk.Frame(root, bg="#F5F5F5", height=100)
header.pack(fill="x")
logo = tk.PhotoImage(file="kiosk.png").subsample(3, 3)
logo_label = tk.Label(header, image=logo, bg="#F5F5F5")
logo_label.pack(side="left")
company_name = tk.Label(header, text="MPATANE KIOSK", font=("Arial", 24), fg="#333333", bg="#F5F5F5")
company_name.pack(expand=True, fill="both")


navbar = tk.Frame(root, bg="#555")
navbar.pack(side="left", fill="y")


def open_inventory():
    inventory_window = tk.Toplevel(root)
    inventory_window.geometry("1000x6700")
    inventory_window.title("Inventory")

    # Retrieve data from the "inventory" table
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM inventory")
    data = cursor.fetchall()

    # Create a canvas to hold the table and a scrollbar
    canvas = tk.Canvas(inventory_window, height=400)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(inventory_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    # Create a table to display the data
    table = tk.Frame(canvas)
    canvas.create_window((0,0), window=table, anchor='nw')

    # Add column headers
    headers = ("InventoryID", "ProductName", "UnitPrice", "Quantity")
    for i, header in enumerate(headers):
        label = tk.Label(table, text=header, font=("Helvetica", 14, "bold"))
        label.grid(row=0, column=i, padx=5, pady=5)

    # Add data to the table
    for row, item in enumerate(data):
        for column, value in enumerate(item):
            label = tk.Label(table, text=value)
            label.grid(row=row+1, column=column, padx=5, pady=5)

    # Update the table automatically when data changes
    def update_table():
        cursor.execute("SELECT * FROM inventory")
        data = cursor.fetchall()
        for widget in table.winfo_children():
            widget.destroy()

        # Add column headers
        headers = ("InventoryID", "ProductName", "UnitPrice", "Quantity")
        for i, header in enumerate(headers):
            label = tk.Label(table, text=header, font=("Helvetica", 14, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5)

        # Add data to the table
        for row, item in enumerate(data):
            for column, value in enumerate(item):
                label = tk.Label(table, text=value)
                label.grid(row=row+1, column=column, padx=5, pady=5)

        inventory_window.after(1000, update_table)

    update_table()

    # Add data rows
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            label = tk.Label(table, text=value, font=("Helvetica", 14))
            label.grid(row=i+1, column=j, padx=5, pady=5)


    inventory_id_label = tk.Label(inventory_window, text="InventoryID", font=("Helvetica", 14))
    inventory_id_label.pack(padx=10, pady=10)
    inventory_id_entry = tk.Entry(inventory_window, font=("Helvetica", 14))
    inventory_id_entry.pack(padx=10, pady=10)

    product_name_label = tk.Label(inventory_window, text="Product Name", font=("Helvetica", 14))
    product_name_label.pack(padx=10, pady=10)
    product_name_entry = tk.Entry(inventory_window, font=("Helvetica", 14))
    product_name_entry.pack(padx=10, pady=10)

    unit_price_label = tk.Label(inventory_window, text="Unit Price", font=("Helvetica", 14))
    unit_price_label.pack(padx=10, pady=10)
    unit_price_entry = tk.Entry(inventory_window, font=("Helvetica", 14))
    unit_price_entry.pack(padx=10, pady=10)

    quantity_label = tk.Label(inventory_window, text="Quantity", font=("Helvetica", 14))
    quantity_label.pack(padx=10, pady=10)
    quantity_entry = tk.Entry(inventory_window, font=("Helvetica", 14))
    quantity_entry.pack(padx=10, pady=10)




#1.	 allow workers to add products.
    def add_product():
        # Get input data from the entry fields
        product_name = product_name_entry.get()
        unit_price = unit_price_entry.get()
        quantity = quantity_entry.get()

        # Insert the data into the "inventory" table
        cursor = mydb.cursor()
        query = "INSERT INTO inventory (ProductName, UnitPrice, Quantity) VALUES (%s, %s, %s)"
        values = (product_name, unit_price, quantity)
        try:
            cursor.execute(query, values)
            mydb.commit()
            # Show a success message
            status_label.config(text="Product saved successfully!", fg="green")
        except Exception as e:
            # Show an error message
            status_label.config(text="Error: " + str(e), fg="red")
            return

        # Refresh the table with the updated data
        cursor.execute("SELECT * FROM inventory")
        data = cursor.fetchall()
        for widget in table.winfo_children():
            widget.destroy()
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                label = tk.Label(table, text=value, font=("Helvetica", 14))
                label.grid(row=i+1, column=j, padx=5, pady=5)

        status_label = tk.Label(root, text="")            




#2.	be able to allow users to update product information.
    def confirm_update():
        # Display a confirmation messagebox
        confirm = messagebox.askyesno("Confirm Update", "Are you sure you want to update the inventory?")

        if confirm:
            # Get the input values
            inventory_id = inventory_id_entry.get()
            product_name = product_name_entry.get()
            unit_price = unit_price_entry.get()
            quantity = quantity_entry.get()

            # Update the inventory table in the database
            sql = "UPDATE inventory SET ProductName=%s, UnitPrice=%s, Quantity=%s WHERE InventoryID=%s"
            values = (product_name, unit_price, quantity, inventory_id)
            cursor.execute(sql, values)
            mydb.commit()

            # Display a success messagebox
            messagebox.showinfo("Update", "Inventory updated successfully!")






#3.	allow workers to delete product information, including product name, description, price, and quantity.
    def delete_product():
        # Open a new window to display the table
        table_window = tk.Toplevel()
        table_window.title("Select a row to delete")
        table_window.geometry("600x400")
        
        # Create a table to display the inventory data
        table_frame = tk.Frame(table_window)
        table_frame.pack(fill=tk.BOTH, expand=True)

        table = ttk.Treeview(table_frame, columns=("InventoryID", "ProductName", "UnitPrice", "Quantity"), show="headings")
        table.heading("InventoryID", text="Inventory ID")
        table.heading("ProductName", text="Product Name")
        table.heading("UnitPrice", text="Unit Price")
        table.heading("Quantity", text="Quantity")

        # Get the data from the inventory table and populate the table
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM inventory")
        rows = cursor.fetchall()
        for row in rows:
            table.insert("", "end", values=row)

        # Add a delete button to delete the selected row
        def delete_selected():
            selection = table.focus()
            if not selection:
                return
            data = table.item(selection)["values"]
            inventory_id = data[0]
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete inventory item with ID {inventory_id}?")
            if confirm:
                try:
                    cursor.execute(f"DELETE FROM inventory WHERE InventoryID={inventory_id}")
                    mydb.commit()
                    messagebox.showinfo("Delete Successful", "Inventory item deleted successfully.")
                    # Refresh the table in the main window
                    #refresh_table(table)
                    # Close the table window
                    table_window.destroy()
                except Exception as e:
                    messagebox.showerror("Delete Error", f"Error deleting inventory item: {e}")

        delete_button = tk.Button(table_window, text="Delete", command=delete_selected)
        delete_button.pack(pady=10)

        table.pack(fill=tk.BOTH, expand=True)

        # Add a cancel button to close the window
        cancel_button = tk.Button(table_window, text="Cancel", command=table_window.destroy)
        cancel_button.pack(pady=10)










    add_btn = tk.Button(inventory_window, text="Add", bg="green", fg="white", font=("Helvetica", 14), relief="flat", command=add_product)
    add_btn.pack(side="left", padx=10, pady=10)


    update_btn = tk.Button(inventory_window, text="Update", bg="orange", fg="white", font=("Helvetica", 14), relief="flat", command=confirm_update)
    update_btn.pack(side="left", padx=10, pady=10)

    delete_btn = tk.Button(inventory_window, text="Delete", bg="red", fg="white", font=("Helvetica", 14), relief="flat", command=delete_product)
    delete_btn.pack(side="left", padx=10, pady=10)

inventory_btn = tk.Button(navbar, text="Inventory", bg="#222", fg="white", font=("Helvetica", 14), relief="flat", command=open_inventory)
inventory_btn.pack(pady=10, padx=10, fill="x")



def make_sale():
    # Create a new window for making a sale
    sale_window = tk.Toplevel(root)
    sale_window.geometry("1000x670")
    sale_window.title("Make Sale")

    # Retrieve data from the "sales" table
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM sales")
    sales_data = cursor.fetchall()

    # Create a canvas to hold the table and a scrollbar
    canvas = tk.Canvas(sale_window, height=400)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(sale_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    # Create a table to display the sales data
    table = tk.Frame(canvas)
    canvas.create_window((0, 0), window=table, anchor='nw')

    # Add column headers
    headers = ("SalesID", "ProductName", "SalesPrice", "InventoryID")
    for i, header in enumerate(headers):
        label = tk.Label(table, text=header, font=("Helvetica", 14, "bold"))
        label.grid(row=0, column=i, padx=5, pady=5)

    # Add data rows
    for row, sale in enumerate(sales_data):
        for column, value in enumerate(sale):
            label = tk.Label(table, text=value)
            label.grid(row=row+1, column=column, padx=5, pady=5)

    # Update the table automatically when data changes
    def update_table():
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()
        for widget in table.winfo_children():
            widget.destroy()

        # Add column headers
        headers = ("SalesID", "ProductName", "SalesPrice", "InventoryID")
        for i, header in enumerate(headers):
            label = tk.Label(table, text=header, font=("Helvetica", 14, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5)

        # Add data rows
        for row, sale in enumerate(sales_data):
            for column, value in enumerate(sale):
                label = tk.Label(table, text=value)
                label.grid(row=row+1, column=column, padx=5, pady=5)

        sale_window.after(1000, update_table)

    update_table()

    # Create labels and entry fields for the sale details

    salesid_label = tk.Label(sale_window, text="SalesID:")
    salesid_label.pack(padx=5, pady=5)
    salesid_entry = tk.Entry(sale_window)
    salesid_entry.pack(padx=5, pady=5)

    product_label = tk.Label(sale_window, text="Product Name:")
    product_label.pack(padx=5, pady=5)
    product_entry = tk.Entry(sale_window)
    product_entry.pack(padx=5, pady=5)

    price_label = tk.Label(sale_window, text="Sales Price:")
    price_label.pack(padx=5, pady=5)
    price_entry = tk.Entry(sale_window)
    price_entry.pack(padx=5, pady=5)







    def add_product():
        # Get input data from the entry fields
        product_name = product_entry.get()
        sales_price = price_entry.get()

        # Insert the data into the "sales" table
        cursor = mydb.cursor()
        query = "INSERT INTO sales (ProductName, SalesPrice) VALUES (%s, %s)"
        values = (product_name, sales_price)
        try:
            cursor.execute(query, values)
            mydb.commit()
            # Show a success message
            status_label.config(text="Product saved successfully!", fg="green")
        except Exception as e:
            # Show an error message
            status_label.config(text="Error: " + str(e), fg="red")
            return

        # Refresh the table with the updated data
        cursor.execute("SELECT * FROM sales")
        sales_data = cursor.fetchall()
        for widget in table.winfo_children():
            widget.destroy()
        for row, sale in enumerate(sales_data):
            for column, value in enumerate(sale):
                label = tk.Label(table, text=value, font=("Helvetica", 14))
                label.grid(row=row+1, column=column, padx=5, pady=5)

        status_label = tk.Label(root, text="")






#4.	 allow workers to update sales information. 
    def confirm_update():
        # Display a confirmation messagebox
        confirm = messagebox.askyesno("Confirm Product", "Are you sure you want to update this product?")

        if confirm:
            # Get the input values
            salesid = salesid_entry.get()
            product_name = product_entry.get()
            sales_price = price_entry.get()

            # Insert the product into the sales table in the database
            sql = "UPDATE sales SET ProductName = %s, SalesPrice = %s WHERE SalesID = %s"
            values = (product_name, sales_price, salesid)
            cursor.execute(sql, values)
            mydb.commit()

            # Display a success messagebox
            messagebox.showinfo("Product Added", "Product added successfully!")







#5.	allow workers to delete sales information.
    def delete_product():
        # Open a new window to display the table
        table_window = tk.Toplevel()
        table_window.title("Select a row to delete")
        table_window.geometry("600x400")
        
        # Create a table to display the sales data
        table_frame = tk.Frame(table_window)
        table_frame.pack(fill=tk.BOTH, expand=True)

        table = ttk.Treeview(table_frame, columns=("SalesID", "ProductName", "SalesPrice"), show="headings")
        table.heading("SalesID", text="Sales ID")
        table.heading("ProductName", text="Product Name")
        table.heading("SalesPrice", text="Sales Price")

        # Get the data from the sales table and populate the table
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM sales")
        rows = cursor.fetchall()
        for row in rows:
            table.insert("", "end", values=row)

        # Add a delete button to delete the selected row
        def delete_selected():
            selection = table.focus()
            if not selection:
                return
            data = table.item(selection)["values"]
            sales_id = data[0]
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete sale with ID {sales_id}?")
            if confirm:
                try:
                    cursor.execute(f"DELETE FROM sales WHERE SalesID={sales_id}")
                    mydb.commit()
                    messagebox.showinfo("Delete Successful", "Sale deleted successfully.")
                    # Refresh the table in the main window
                    # refresh_table(table)
                    # Close the table window
                    table_window.destroy()
                except Exception as e:
                    messagebox.showerror("Delete Error", f"Error deleting sale: {e}")










        delete_button = tk.Button(table_window, text="Delete", command=delete_selected)
        delete_button.pack(pady=10)

        table.pack(fill=tk.BOTH, expand=True)

        # Add a cancel button to close the window
        cancel_button = tk.Button(table_window, text="Cancel", command=table_window.destroy)
        cancel_button.pack(pady=10)


    add_btn = tk.Button(sale_window, text="Add", bg="green", fg="white", font=("Helvetica", 14), relief="flat", command=add_product)
    add_btn.pack(side="left", padx=10, pady=10)


    update_btn = tk.Button(sale_window, text="Update", bg="orange", fg="white", font=("Helvetica", 14), relief="flat", command=confirm_update)
    update_btn.pack(side="left", padx=10, pady=10)

    delete_btn = tk.Button(sale_window, text="Delete", bg="red", fg="white", font=("Helvetica", 14), relief="flat", command=delete_product)
    delete_btn.pack(side="left", padx=10, pady=10)



sales_btn = tk.Button(navbar, text="Sales", bg="#222", fg="white", font=("Helvetica", 14), relief="flat", command=make_sale)
sales_btn.pack(pady=10, padx=10, fill="x")







root.main_frame = tk.Frame()
root.main_frame.pack(fill=tk.BOTH, expand=True)





#6.	allow workers to track the quantity of products in stock. 
# Create inventory frame
root.inventory_box = tk.LabelFrame(root.main_frame, text="Inventory", padx=10, pady=10)
root.inventory_box.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

# Create a new Frame inside the inventory_box
inventory_frame = tk.Frame(root.inventory_box)
inventory_frame.pack(fill=tk.BOTH, expand=True)

# Create a Treeview widget inside the inventory_frame
inventory_tree = ttk.Treeview(inventory_frame, columns=("ProductName", "Quantity"), show="headings")
inventory_tree.column("ProductName", width=200)
inventory_tree.column("Quantity", width=100)
inventory_tree.heading("ProductName", text="Product Name")
inventory_tree.heading("Quantity", text="Quantity")
inventory_tree.pack(fill=tk.BOTH, expand=True)

# Query the database and insert the results into the Treeview
mycursor = mydb.cursor()
mycursor.execute("SELECT ProductName, Quantity FROM inventory")
results = mycursor.fetchall()

for result in results:
    inventory_tree.insert("", "end", values=result)









# Create sales frame
root.sales_box = tk.LabelFrame(root.main_frame, text="Sales", padx=10, pady=10)
root.sales_box.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NSEW)

# Create a new Frame inside the sales_box
sales_frame = tk.Frame(root.sales_box)
sales_frame.pack(fill=tk.BOTH, expand=True)

# Create a Treeview widget inside the sales_frame
sales_tree = ttk.Treeview(sales_frame, columns=("Products", "Quantity"), show="headings")
sales_tree.column("Products", width=200)
sales_tree.column("Quantity", width=100)
sales_tree.heading("Products", text="Product Name")
sales_tree.heading("Quantity", text="Quantity")
sales_tree.pack(fill=tk.BOTH, expand=True)

# Query the database and insert the results into the Treeview
mycursor.execute("SELECT ProductName, COUNT(InventoryID) as Quantity FROM sales WHERE InventoryID IN (SELECT InventoryID FROM inventory) GROUP BY ProductName")
results = mycursor.fetchall()

for result in results:
    sales_tree.insert("", "end", values=result)










#8.	allow workers to analyse sales trends for individual products and identify which products are selling the most.
# Create analysis frame
root.analysis_box = tk.LabelFrame(root.main_frame, text="Analysis", padx=10, pady=10)
root.analysis_box.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)

#15.	Use python to visualise the data.
# Create a Figure object
fig = plt.Figure(figsize=(5, 4), dpi=100)

ax = fig.add_subplot(111)

x = []
y = []
for item in sales_tree.get_children():
    values = sales_tree.item(item)["values"]
    x.append(values[0])
    y.append(values[1])
ax.barh(x, y)

ax.set_xlabel('Quantity')

fig.tight_layout()

canvas = FigureCanvasTkAgg(fig, master=root.analysis_box)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)







# Configure the rows and columns
root.main_frame.rowconfigure(0, weight=1)
root.main_frame.rowconfigure(1, weight=3)
root.main_frame.columnconfigure(0, weight=1)
root.main_frame.columnconfigure(1, weight=1)






# Define function to refresh data
def refresh_data():
    # Clear the Treeviews
    inventory_tree.delete(*inventory_tree.get_children())
    sales_tree.delete(*sales_tree.get_children())

    # Query the database and insert the results into the Treeviews
    mycursor.execute("SELECT ProductName, Quantity FROM inventory")
    inventory_results = mycursor.fetchall()
    for result in inventory_results:
        inventory_tree.insert("", "end", values=result)

    mycursor.execute("SELECT ProductName, COUNT(InventoryID) as Quantity FROM sales WHERE InventoryID IN (SELECT InventoryID FROM inventory) GROUP BY ProductName")
    sales_results = mycursor.fetchall()
    for result in sales_results:
        sales_tree.insert("", "end", values=result)

    # Update the plot in the analysis box
    update_plot()

def update_plot():
    # Clear the plot
    ax.clear()

    # Get the data from the sales_tree and create a horizontal bar chart
    x = []
    y = []
    for item in sales_tree.get_children():
        values = sales_tree.item(item)["values"]
        x.append(values[0])
        y.append(values[1])
    ax.barh(x, y)


    # Set x-axis label
    ax.set_xlabel('Quantity')

    # Adjust the position of the subplots and axis labels
    fig.tight_layout()

    # Redraw the canvas
    canvas.draw()





# Create refresh button
refresh_btn = tk.Button(navbar, text="Refresh", bg="#222", fg="white", font=("Helvetica", 14), relief="flat", command=refresh_data)
refresh_btn.pack(pady=10, padx=10, fill="x")


# Create confirmation popup window function
def confirm_logout():
    confirm = tk.messagebox.askyesno("Confirm Logout", "Are you sure you want to quit?")
    if confirm:
        root.destroy()

# Create logout button
logout_btn = tk.Button(navbar, text="Logout", bg="#222", fg="white", font=("Helvetica", 14), relief="flat", command=confirm_logout)
logout_btn.pack(side=tk.BOTTOM, pady=10, padx=10, fill="x")

root.mainloop()
