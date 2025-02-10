#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 10:06:40 2024

@author: jakobfick
"""

# login_gui.py
import tkinter as tk
from tkinter import messagebox

class ManagerLoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)  # Initialize the frame
        self.parent = parent
        self.controller = controller  # Store a reference to the controller
        self.configure(width=300, height=300)
        self.widgets()

    def widgets(self):
        welcome = tk.Label(self, text="Welcome to the Login Screen!")
        welcome.grid(row=0, column=0, columnspan=2, sticky="w", pady=10)

        UN_label = tk.Label(self, text="Username:")
        UN_label.grid(row=1, column=0, sticky="w")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        PW_label = tk.Label(self, text="Password:")
        PW_label.grid(row=2, column=0, sticky="w")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, pady=10)

        login_button = tk.Button(self, text="Login", command=self.validate_login)
        login_button.grid(row=3, column=0, columnspan=2, pady=10)

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print("1")
        print(username)
        print(password)

        # Pass username and password to the main controller for validation
        self.controller.validate_credentials(username, password)

    def show_error(self, message):
        """Displays an error message if login fails."""
        messagebox.showerror("Login Failed", message)

    def show_success(self, first_name, last_name):
        """Displays a success message if login is successful."""
        messagebox.showinfo("Login Successful", f"Welcome, {first_name} {last_name}!")
        self.controller.show_dashboard()  # Switch to the dashboard after login
        
    def clear_text(self):
        self.username_entry.delete("0", "end")
        self.password_entry.delete("0", "end")


'''    
# Create main application window
root = tk.Tk()
root.title("Employee Login")
root.geometry("660x700")

#creating the frame that will contain the login screen
frame = ManagerloginFrame(root)
frame.grid()

# Run the main event loop
root.mainloop()
'''