#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 18:40:15 2024

@author: jakobfick
"""

import tkinter as tk
from tkinter import messagebox

#This class is the search for supperior frame. This frame will be displayed after a system manager chooses to add a new
#employee to the database. The frame will provide a textboxes that will let the system manager search the database for a
#employee using their username. The manager can use this frame to select the new employees supperior.
class searchSubordinateFrame(tk.Frame):
    
    #constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #, bg="red")
        
        self.controller = controller
        
        # Calling the method that will create the different widgets in the frame
        self.widgets()
    
    #creating all the different widgets in the frame
    def widgets(self):
        instructions = tk.Label(self, text="Enter username of employee's subordinate!")
        instructions.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        name_Label = tk.Label(self, text="Username: ")
        name_Label.grid(row=2, column=0, padx=10, pady=10)
        self.name_text = tk.Entry(self, width=20)
        self.name_text.grid(row=2, column=1, padx=10)
        
        search_Button = tk.Button(self, text="Search", command=self.search)
        search_Button.grid(row=5, column=0, pady=20)
        done_Button = tk.Button(self, text="Done", command=self.done)
        done_Button.grid(row=5, column=1, pady=20)
        
    #When the search button is pressed, this method will call a method in the Manager_Main controller
    #and send the username so it can be searched for in the database
    def search(self):
        username = self.name_text.get()
        self.controller.add_employee_subordinate(username)
        
    #Finishing the new employee file and adding it to the database
    def done(self):
        self.controller.review_new_employee()
        
    def show_error(self, message):
        """Displays an error message if the superior couldn't be found."""
        messagebox.showerror("Search Failed", message)
        
    def show_success(self, message):
        """Displays an error message if the superior couldn't be found."""
        messagebox.showerror("Search Successful", message)
        self.name_text.delete(0, tk.END)

'''
# Create main application window
root = tk.Tk()
root.title("Select Subordinate")
root.geometry("660x700")

#creating the frame that will contain the login screen
frame = searchSubordinateFrame(root)
frame.grid()

# Run the main event loop
root.mainloop()
'''