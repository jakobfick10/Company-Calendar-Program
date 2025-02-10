#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 22:15:04 2024

@author: jakobfick
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
from functools import partial

class customerTimeFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller
        
        # Creating the canvas that will contain the day screen
        self.canvas = tk.Canvas(self, width=600, height=500)
        self.canvas.grid(row=2, column=0, rowspan=4, sticky="nsew") 

        # Create a scrollbar widget
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=2, column=1, rowspan=4, sticky="ns")

        # Attach the scrollbar to the canvas
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Creating the inner frame inside the canvas
        self.time_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.time_frame, anchor="nw")
        
        # Ensure the canvas scrolls properly
        self.time_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.widgets()
    
    def widgets(self):
        # Give the user instructions
        instructions = ttk.Label(self, text="Select the time you would like to have the meeting\nand the representative you would like to meet with.")
        instructions.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        
    def display_times(self, representatives, date):
        num = 2
        
        for rep in representatives:
            rep_name = ttk.Label(self.time_frame, text=rep.get("FirstName")+" "+rep.get("LastName"))
            rep_name.grid(row=num, column=1, padx=20, pady=10)
            num += 1
            
            for time in rep.get("Slots"):
                time_button = ttk.Button(self.time_frame, text=time, command=partial(self.choose_time, rep.get("EmployeeID"), time, date))
                time_button.grid(row=num, column=1, padx=20, pady=2)
                num += 1

    def choose_time(self, rep_ID, time, date):
        self.controller.add_meeting(rep_ID, time, date)
        print(time)

'''
# Testing the frame
if __name__ == "__main__":
    root = tk.Tk()
    frame = customerTimeFrame(root, None)
    frame.grid(row=0, column=0, sticky="nsew")

    # Example representatives data
    representatives = [
        {"FirstName": "John", "LastName": "Doe", "EmployeeID": "1", "Slots": ["10:00 AM", "10:30 AM"]},
        {"FirstName": "Jane", "LastName": "Smith", "EmployeeID": "2", "Slots": ["11:00 AM", "11:30 AM"]}
    ]
    frame.display_times(representatives, "2023-04-07")

    root.mainloop()
    '''
