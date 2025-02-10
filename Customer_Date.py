#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 14:03:51 2024

@author: jakobfick
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime

#After the customer selects to schedule a meeting with a company representative this frame will be displayed.
#This frame will let the customer select the date they would like to have a meeting.
class customerDateFrame(tk.Frame):
    
    #constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #, bg="red")
        
        self.controller = controller
        
        #Placing this frame (CreateEventFrame) inside the widow
        #self.pack(fill="both", expand=1)
        
        # Calling the method that will create the different widgets in the frame
        self.widgets()
    
    #creating all the different widgets in the frame
    def widgets(self):
        # Give the user instructions
        instructions = ttk.Label(self, text="Select the date you would like to\nschedule the meeting on.")
        instructions.grid(row=1, pady=10)
        
        # Create Calendar widget
        self.cal = Calendar(self, selectmode="day") #, year=2024, month=4, day=22)
        self.cal.grid(row = 3, pady=10)

        # Create button to show selected date
        show_date_button = ttk.Button(self, text="Select Date", command=self.check_selected_date)
        show_date_button.grid(row=5, pady=5)

        # Label to display selected date
        self.selected_date_label = ttk.Label(self, text="")
        self.selected_date_label.grid(row = 7, pady=5)

    def check_selected_date(self):
        selected_date = self.cal.get_date()
        #self.selected_date_label.config(text="Selected Date: " + self.selected_date)
        self.controller.find_meeting_times(datetime.strptime(selected_date, "%m/%d/%y"))


'''
# Create main application window
root = tk.Tk()
root.title("Customer Menu")
root.geometry("660x700")

#creating the frame that will contain the login screen
frame = customerDateFrame(root)
frame.grid()

# Run the main event loop
root.mainloop()
'''
