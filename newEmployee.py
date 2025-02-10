#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 22:32:30 2024

@author: jakobfick
"""

import tkinter as tk
from tkinter import messagebox

#This class is the new employee frame. This frame will be displayed after a system manager chooses to add a new
#employee to the database. The frame will provide textboxes and dropdown menues that will let the system manager
#enter information about the new employee.
class newEmployeeFrame(tk.Frame):
    
    #constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #, bg="red")
        
        self.controller = controller
        
        #setting the options for the different employee roles
        self.roles = ["Accountant", "Advisor", "Programmer", "System Manager", "Company Representative"]
        
        #creating the text variable the selected role will be stored as
        self.roleSelected = tk.StringVar()
        self.roleSelected.set("")
        
        # Calling the method that will create the different widgets in the frame
        self.widgets()
    
    #creating all the different widgets in the frame
    def widgets(self):
        instructions = tk.Label(self, text="Enter new employee information")
        instructions.grid(row=0, column=0, columnspan=2, pady=10)
        
        first_name_Label = tk.Label(self, text="First Name: ")
        first_name_Label.grid(row=1, column=0)
        self.first_name_Text = tk.Entry(self, width=20)
        self.first_name_Text.grid(row=1, column=1)
        
        last_name_Label = tk.Label(self, text="Last Name: ")
        last_name_Label.grid(row=2, column=0)
        self.last_name_Text = tk.Entry(self, width=20)
        self.last_name_Text.grid(row=2, column=1)
        
        user_Label = tk.Label(self, text="Username: ")
        user_Label.grid(row=3, column=0)
        self.user_Text = tk.Entry(self, width=20)
        self.user_Text.grid(row=3, column=1)
        
        pass_Label = tk.Label(self, text="Password: ")
        pass_Label.grid(row=4, column=0)
        self.pass_Text = tk.Entry(self, width=20)
        self.pass_Text.grid(row=4, column=1)
        
        role_Label = tk.Label(self, text="Role: ")
        role_Label.grid(row=5, column=0)
        self.role_Menu = tk.OptionMenu(self, self.roleSelected, *self.roles)
        self.role_Menu.grid(row=5, column=1, sticky="w")
        
        next_Button = tk.Button(self, text="Next", command=self.add_employee)
        next_Button.grid(row=6, column=0, pady=20)
        
    #When the next button is pressed, the information added will be recorded and saved
    def add_employee(self):
        first_name = self.first_name_Text.get()
        last_name = self.last_name_Text.get()
        username = self.user_Text.get()
        password = self.pass_Text.get()
        role = self.roleSelected.get()
        self.controller.add_employee_1(first_name, last_name, username, password, role)
        
        

