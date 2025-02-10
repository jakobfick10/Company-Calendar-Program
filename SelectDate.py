#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 08:04:59 2024

@author: jakobfick
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta

# This class is the Select Date frame. This frame will be displayed after a user presses a button to 
# select a date. This frame will display a calendar in which each day is a button and by pressing a
#date, the user can select what date they want to view.
class selectDateFrame(tk.Frame):
    
    # Constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #initializing the 'main' class as the controller
        self.controller = controller
        '''
        #Placing this frame (selectDateFrame) inside the widow
        self.pack(fill="both", expand=1)
        '''
        # Create an object to hold the selected date
        self.selected_date = datetime.date
        
        # Calling the method that will create the different widgets in the frame
        self.widgets()
    
    #creating all the different widgets in the frame
    def widgets(self):   
        # Creating the label that will instruct the user to select a date
        instructions = tk.Label(self, text="Select the date you wish to view!")
        instructions.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # Create Calendar widget
        self.cal = Calendar(self, selectmode="day")
        self.cal.grid(row = 1, pady=10)
        
        # Label to display selected date
        self.selected_date_label = ttk.Label(self, text="")
        self.selected_date_label.grid(row = 2, pady=5)
        
        # Create button to show selected date
        show_date_button = ttk.Button(self, text="Show Selected Date", command=self.show_selected_date)
        show_date_button.grid(row = 3, pady=5)
    
    #This method will be called if the select button is pressed, call the function in the main class
    #that will pull up the day screen for the selected date.
    def show_selected_date(self):
        self.selected_date = self.cal.get_date()
        #self.selected_date_label.config(text="Selected Date: " + self.selected_date)
        selected_date = datetime.strptime(self.selected_date, "%m/%d/%y") #.strftime('%Y-%m-%d')
        self.controller.show_date(selected_date)
        
        
        
                   
'''
# Create main application window
root = tk.Tk()
root.title("Select Date")
root.geometry("660x700")

#creating the frame that will contain the login screen
frame = selectDateFrame(root)

# Run the main event loop
root.mainloop()
'''