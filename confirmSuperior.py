#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 17:02:43 2024

@author: jakobfick
"""

import tkinter as tk
from tkinter import messagebox

#This class is the confirm superior frame. This frame will be displayed after a system manager chooses to add a new
#employee to the database. After the system manager searches for the new employees superior, the system will search
#the database for the username entered. If a matching username is found in the database, the information of the employee
#found will be displayed in this frame. This frame will allow the user to confirm is the employee found is the correct one.
class confirmSuperiorFrame(tk.Frame):
    
    #constructor
    def __init__(self, parent, data):
        tk.Frame.__init__(self, parent) #, bg="red")
        
        #adding the superior data that was sent to the frame as input (data)
        self.data = data
        
        #Placing this frame (CreateEventFrame) inside the widow
        self.pack(fill="both", expand=1)
        
        # Calling the method that will create the different widgets in the frame
        self.widgets()
    
    #creating all the different widgets in the frame
    def widgets(self):
        instructions = tk.Label(self, text="Is the following information correct?")
        instructions.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        #displaying the superiors username
        user_Label = tk.Label(self, text="Username: ")
        user_Label.grid(row=2, column=0, pady=5)
        user = tk.Label(self, text=data["username"])
        user.grid(row=2, column=1)
        
        #displaying the superiors name
        name_Label = tk.Label(self, text="Name: ")
        name_Label.grid(row=3, column=0, pady=5)
        name = tk.Label(self, text=data["name"])
        name.grid(row=3, column=1)
        
        #displaying the superiors position
        position_Label = tk.Label(self, text="Position: ")
        position_Label.grid(row=4, column=0, pady=5)
        position = tk.Label(self, text=data["position"])
        position.grid(row=4, column=1)
        
        confirm_Button = tk.Button(self, text="Confirm")
        confirm_Button.grid(row=5, column=0, pady=20)
        cancel_Button = tk.Button(self, text="Cancel")
        cancel_Button.grid(row=5, column=1, pady=20)

        
#The data of the searched superior retrieved from the database
data = {"name":"Jakob Fick", "username":"jfick21", "position":"Student"}

# Create main application window
root = tk.Tk()
root.title("Select Subordinate")
root.geometry("660x700")

#creating the frame that will contain the login screen
frame = confirmSuperiorFrame(root, data)
frame.grid()

# Run the main event loop
root.mainloop()