#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 16:38:53 2024

@author: jakobfick
"""

import tkinter as tk
from tkinter import messagebox

#This class is the Manager menu frame. This frame will be displayed after a system manager logs into the system
#manager program. The screen will allow the system manager to select which action they would like to perform.
#The options will be displayed as 3 buttons: a add employee button, remove employee button, and logout button.
class managerMenuFrame(tk.Frame):
    
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
        instructions = tk.Label(self, text="Select an Option")
        instructions.grid(row=0, pady=10)
        
        addEmployee = tk.Button(self, text="Add an Employee", command=self.controller.show_new_employee)
        addEmployee.grid(row=1, padx=10, pady=10)
        
        removeEmployee = tk.Button(self, text="Remove an Employee", command=self.controller.show_search)
        removeEmployee.grid(row=2, padx=10, pady=10)
        
        logout = tk.Button(self, text="Logout", command=self.controller.logout)
        logout.grid(row=3, padx=10, pady=10)
        
'''
# Create main application window
root = tk.Tk()
root.title("Select Subordinate")
root.geometry("660x700")

#creating the frame that will contain the login screen
frame = managerMenuFrame(root)
frame.grid()

# Run the main event loop
root.mainloop()
'''