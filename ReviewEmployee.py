#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 20:03:41 2024

@author: jakobfick
"""

import tkinter as tk
from tkinter import messagebox

#This class is the search for supperior frame. This frame will be displayed after a system manager chooses to add a new
#employee to the database. The frame will provide a textboxes that will let the system manager search the database for a
#employee using their username. The manager can use this frame to select the new employees supperior.
class reviewEmployeeFrame(tk.Frame):
    
    #constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #, bg="red")
        
        self.controller = controller
        
        #Placing this frame (CreateEventFrame) inside the widow
        #self.pack(fill="both", expand=1)
    
    #creating all the different widgets in the frame
    def show_employee(self, data):
        #adding the superior data that was sent to the frame as input (data)
        self.data = data
        
        instructions = tk.Label(self, text="Confirm the Employee information is correct.")
        instructions.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        #Displaying the new employees information
        name_Label = tk.Label(self, text="Name: ")
        name_Label.grid(row=2, column=0, padx=10)
        Fname_text = tk.Label(self, text=self.data["FirstName"] + " " + self.data["LastName"])
        Fname_text.grid(row=2, column=1, padx=10)
        #Lname_text = tk.Label(self, text=self.data["LastName"])
        #Lname_text.grid(row=2, column=2, padx=10)
        
        user_Label = tk.Label(self, text="Userame: ")
        user_Label.grid(row=3, column=0, padx=10)
        user_text = tk.Label(self, text=self.data["Email"])
        user_text.grid(row=3, column=1, padx=10)
                
        pass_Label = tk.Label(self, text="Password: ")
        pass_Label.grid(row=4, column=0, padx=10)
        pass_text = tk.Label(self, text=self.data["Password"])
        pass_text.grid(row=4, column=1, padx=10)
                
        posi_Label = tk.Label(self, text="Position: ")
        posi_Label.grid(row=5, column=0, padx=10)
        posi_text = tk.Label(self, text=self.data["Position"])
        posi_text.grid(row=5, column=1, padx=10)
        
        #Displaying the information of the employee's superior
        superior_Label = tk.Label(self, text="Superior")
        superior_Label.grid(row=6, column=0, padx=10, pady=10)
        
        if self.data["Manager"]: 
            sup_name_Label = tk.Label(self, text="Name: ")
            sup_name_Label.grid(row=7, column=0, padx=10)
            Fsup_name_text = tk.Label(self, text=self.data["Manager"]["FirstName"] + " " + self.data["Manager"]["LastName"])
            Fsup_name_text.grid(row=7, column=1, padx=10)
            #Lsup_name_text = tk.Label(self, text=self.data["Manager"]["LastName"])
            #Lsup_name_text.grid(row=7, column=2, padx=10)
        
            sup_user_Label = tk.Label(self, text="Username: ")
            sup_user_Label.grid(row=8, column=0, padx=10)
            sup_user_text = tk.Label(self, text=self.data["Manager"]["Email"])
            sup_user_text.grid(row=8, column=1, padx=10)
        
            sup_posi_Label = tk.Label(self, text="Position: ")
            sup_posi_Label.grid(row=9, column=0, padx=10)
            sup_posi_text = tk.Label(self, text=self.data["Manager"]["Position"])
            sup_posi_text.grid(row=9, column=1, padx=10)
            
        else:
            sup_label = tk.Label(self, text="None")
            sup_label.grid(row=7, padx=10)
        
        #Displaying the information of the employee's subordinates if they have any
        #This number tracks how many subordinates the employee has.
        num = 0
        print(len(self.data['Subordinates']))
        print(self.data['Subordinates'])
        if len(self.data["Subordinates"]) != 0:
            num = len(self.data["Subordinates"])
            for i in range(0, num):
                subordinate_Label = tk.Label(self, text="Subordinate " + str(i+1))
                subordinate_Label.grid(row=(4*i)+10, column=0, padx=10, pady=10)
                
                sub_name_Label = tk.Label(self, text="Name: ")
                sub_name_Label.grid(row=(4*i)+11, column=0, padx=10)
                Fsub_name_text = tk.Label(self, text=self.data["Subordinates"][i]["FirstName"] + " " + self.data["Subordinates"][i]["LastName"])
                Fsub_name_text.grid(row=(4*i)+11, column=1, padx=10)
                #Lsub_name_text = tk.Label(self, text=self.data["Subordinates"][i]["LastName"])
                #Lsub_name_text.grid(row=(4*i)+11, column=1, padx=10)
                
                sub_user_Label = tk.Label(self, text="Username: ")
                sub_user_Label.grid(row=(4*i)+12, column=0, padx=10)
                sub_user_text = tk.Label(self, text=self.data["Subordinates"][i]["Email"])
                sub_user_text.grid(row=(4*i)+12, column=1, padx=10)
                
                sub_posi_Label = tk.Label(self, text="Position: ")
                sub_posi_Label.grid(row=(4*i)+13, column=0, padx=10)
                sub_posi_text = tk.Label(self, text=self.data["Subordinates"][i]["Position"])
                sub_posi_text.grid(row=(4*i)+13, column=1, padx=10)
        
            search_Button = tk.Button(self, text="Confirm", command=self.controller.final_add_employee)
            search_Button.grid(row=(num*4)+14, column=0, pady=20)
            cancel_Button = tk.Button(self, text="Cancel", command=self.controller.show_menu)
            cancel_Button.grid(row=(num*4)+14, column=1, pady=20)
        
        #if the new employee has no subordinates
        else:   
            sub_label = tk.Label(self, text="Subordinates")
            sub_label.grid(row=10, padx=10)
            
            sub_label = tk.Label(self, text="None")
            sub_label.grid(row=11, padx=10, pady=10)
            
            search_Button = tk.Button(self, text="Confirm", command=self.controller.final_add_employee)
            search_Button.grid(row=13, column=0, pady=20)
            cancel_Button = tk.Button(self, text="Cancel", command=self.controller.show_menu)
            cancel_Button.grid(row=13, column=1, pady=20)


'''
#The data of the new employee that is being added to the system
superior = {"name":"Bob", "username":"bobby12", "password":"0987", "position":"Teacher"}
sub1 = {"name":"Mike", "username":"mikey12", "password":"9876", "position":"friend"}
sub2 = {"name":"Jeff", "username":"jeffy12", "password":"8765", "position":"friend"}

data = {"name":"Jakob Fick", "username":"jfick21", "password":"123456", "position":"Student", "superior":superior, "subordinates":[sub1, sub2]}
        
# Create main application window
root = tk.Tk()
root.title("Select Subordinate")
root.geometry("660x700")

#creating the frame that will contain the login screen
frame = reviewEmployeeFrame(root, data)
frame.grid()

# Run the main event loop
root.mainloop()
'''