#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 11:12:29 2024

@author: jakobfick
"""

import tkinter as tk
from tkinter import messagebox

#This class is the search for supperior frame. This frame will be displayed after a system manager chooses to add a new
#employee to the database. The frame will provide a textboxes that will let the system manager search the database for a
#employee using their username. The manager can use this frame to select the new employees supperior.
class searchEmployeeFrame(tk.Frame):
    
    #constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #, bg="red")
        
        self.controller = controller
        
        # Calling the method that will create the different widgets in the frame
        self.widgets()
    
    #creating all the different widgets in the frame
    def widgets(self):
        instructions = tk.Label(self, text="Enter username of employee!")
        instructions.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        name_Label = tk.Label(self, text="Username: ")
        name_Label.grid(row=2, column=0, padx=10, pady=10)
        self.name_text = tk.Entry(self, width=20)
        self.name_text.grid(row=2, column=1, padx=10)
        
        search_Button = tk.Button(self, text="Search", command=self.search)
        search_Button.grid(row=5, column=0, pady=20)
        cancel_Button = tk.Button(self, text="Done", command=self.controller.show_menu)
        cancel_Button.grid(row=5, column=1, pady=20)
    
    #When the search button is pressed, this method will call the controller to search the database for the selected employee
    def search(self):
        email = self.name_text.get()
        if email.strip():  # strip() removes leading/trailing spaces
            self.controller.search_employee(email)
    
    #Displaying an error message if the employee could not be found
    def show_error(self, message):
        messagebox.showerror("Error", message)
        
        
'''
# Create main application window
root = tk.Tk()
root.title("Select Subordinate")
root.geometry("660x700")

#creating the frame that will contain the login screen
frame = searchEmployeeFrame(root)
frame.grid()

# Run the main event loop
root.mainloop()
'''