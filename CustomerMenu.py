#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 09:20:21 2024

@author: jakobfick
"""

import tkinter as tk
from tkinter import messagebox

#This class is the Customer menu frame. This frame will be displayed after a Customer manager logs into the 
#company website. The screen will allow the customer to select to schedule a virtual meeting with a company
#representative.
class customerMenuFrame(tk.Frame):
    
    #constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #, bg="red")
        
        self.controller = controller
        self.parent = parent
        
        #Placing this frame (CreateEventFrame) inside the widow
        #self.pack(fill="both", expand=1)
        
        # Calling the method that will create the different widgets in the frame
        self.widgets()
    
    #creating all the different widgets in the frame
    def widgets(self):
        self.message = tk.Label(self, text="")
        self.message.grid(row=0, pady=10)
        
        instructions = tk.Label(self, text="Select an Option")
        instructions.grid(row=1, pady=10)
        
        scheduleMeeting = tk.Button(self, text="Schedule a Meeting\nwith a representative", command=self.controller.show_date)
        scheduleMeeting.grid(row=2, padx=10, pady=10)
        
        #Exit = tk.Button(self, text="Remove an Employee", command=self.controller.show_search)
        #Exit.grid(row=2, padx=10, pady=10)
        
        #Exit = tk.Button(self, text="Exit", command=self.Exit)
        #Exit.grid(row=3, padx=10, pady=10)
        
    def Exit(self):
        self.destroy()
        self.parent.destroy()
        #self.destroy()
        
    def display_success(self):
        self.message.config(text="Your Meeting has been\nScheduled!")
        self.message.config(fg="green")
        
    def display_failure(self):
        self.message.config(text="An Error has occured!")
        self.message.config(fg="red")
        
'''
# Create main application window
root = tk.Tk()
root.title("Customer Menu")
root.geometry("660x700")

#creating the frame that will contain the login screen
frame = customerMenuFrame(root)
frame.grid()

# Run the main event loop
root.mainloop()
'''