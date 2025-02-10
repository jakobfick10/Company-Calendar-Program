#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 22:07:17 2024

@author: jakobfick
"""

import tkinter as tk
from tkinter import messagebox
from functools import partial

#This class is the select subordinate frame. This frame will be displayed when a user selects to view the
#calendar of one of their subordinates. The screen will allow the user to choose which subordinate they would
#like to view. Each subordinate the user has listed under them in the database will be displayed as a button.
# if the user has no subordinates, then an error message will be displayed.
class selectSubordinateFrame(tk.Frame):
    
    #constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #, bg="red")
        self.controller = controller
        
        self.parent = parent
        self.configure(width=300)
        #self.widgets(self.subordinates)
    
    #creating all the different widgets in the login frame
    def widgets(self, subordinates):      
        # Creating the label that will welcome the user to the program
        instruction = tk.Label(self, text="Select the subordinate you wish to view.")
        instruction.grid(row=0, column=0, columnspan=2, sticky="w", pady=10)
        
        buttonNum = 1
        
        #testing if the user has any subordinates
        #if the user has no subordinates:
        if len(subordinates) == 0:
            none = tk.Label(self, text="You have no subordinates listed under you!")
            none.grid(row=2, columnspan= 3, pady=10)
        
        #if the user has at least 1 subordinate:
        else:
            print("Length")
            print(len(subordinates))
            #Creating a button for each subordinate the user has
            for subordinate in subordinates:
                name = f"{subordinate['first_name']} {subordinate['last_name']}"
                employee_id = subordinate['employee_id']
                
                button = tk.Button(self, text=name, command=partial(self.controller.display_subordinates, employee_id))
                button.grid(row=buttonNum)
                buttonNum = buttonNum + 1
                
        cancel = tk.Button(self, text="Cancel", fg="red")
        cancel.grid(row=buttonNum+2, pady=30)

        
    def create(self, ID):
        print(ID)
            

'''
# Create main application window
root = tk.Tk()
root.title("Select Subordinate")
root.geometry("660x700")

#creating the frame that will contain the login screen
frame = selectSubordinateFrame(root)
frame.grid()

# Run the main event loop
root.mainloop()
'''