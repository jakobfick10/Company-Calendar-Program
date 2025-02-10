#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 10:53:07 2024

@author: jakobfick
"""

import tkinter as tk
from tkinter import messagebox

#This class is the search for supperior frame. This frame will be displayed after a system manager chooses to add a new
#employee to the database. The frame will provide a textboxes that will let the system manager search the database for a
#employee using their username. The manager can use this frame to select the new employees supperior.
class deleteEmployeeFrame(tk.Frame):
    
    #constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #, bg="red")
        
        self.controller = controller
        
        # Calling the method that will create the different widgets in the frame
        #self.widgets()
        
        instructions = tk.Label(self, text="Confirm the Employee information is correct.")
        instructions.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        #the frame that will contain all the selected employee's information
        self.info_frame = tk.Frame(self)
        self.info_frame.grid(row=2)
        
    #adding the employee data that was sent to the frame as input (data)
    def set_data(self, employee):
        self.data = employee
        print(self.data)
    
    #creating all the different widgets in the frame
    #they will be placed in the info frame so they can easily be removed
    def widgets(self):
        #Displaying the new employees information
        name_Label = tk.Label(self.info_frame, text="Name: ")
        name_Label.grid(row=2, column=0, padx=10)
        name_text = tk.Label(self.info_frame, text=self.data['Employee']["FirstName"] + " " + self.data['Employee']["LastName"])
        name_text.grid(row=2, column=1, padx=10)
        
        user_Label = tk.Label(self.info_frame, text="Userame: ")
        user_Label.grid(row=3, column=0, padx=10)
        user_text = tk.Label(self.info_frame, text=self.data['Employee']["Username"])
        user_text.grid(row=3, column=1, padx=10)
                
        pass_Label = tk.Label(self.info_frame, text="Password: ")
        pass_Label.grid(row=4, column=0, padx=10)
        pass_text = tk.Label(self.info_frame, text=self.data['Employee']["Password"])
        pass_text.grid(row=4, column=1, padx=10)
                
        posi_Label = tk.Label(self.info_frame, text="Position: ")
        posi_Label.grid(row=5, column=0, padx=10)
        posi_text = tk.Label(self.info_frame, text=self.data['Employee']["Position"])
        posi_text.grid(row=5, column=1, padx=10)
        
        if self.data['Manager']:
            #Displaying the information of the employee's superior
            superior_Label = tk.Label(self.info_frame, text="Superior")
            superior_Label.grid(row=6, column=0, padx=10, pady=10)
            
            sup_name_Label = tk.Label(self.info_frame, text="Name: ")
            sup_name_Label.grid(row=7, column=0, padx=10)
            sup_name_text = tk.Label(self.info_frame, text=self.data["Manager"]["FirstName"] + " " + self.data["Manager"]["LastName"])
            sup_name_text.grid(row=7, column=1, padx=10)
            
            sup_user_Label = tk.Label(self.info_frame, text="Username: ")
            sup_user_Label.grid(row=8, column=0, padx=10)
            sup_user_text = tk.Label(self.info_frame, text=self.data["Manager"]["Username"])
            sup_user_text.grid(row=8, column=1, padx=10)
            
            sup_posi_Label = tk.Label(self.info_frame, text="Position: ")
            sup_posi_Label.grid(row=9, column=0, padx=10)
            sup_posi_text = tk.Label(self.info_frame, text=self.data["Manager"]["Position"])
            sup_posi_text.grid(row=9, column=1, padx=10)
        
        num = 0
        print(len(self.data['Subordinates']))
        print(self.data['Subordinates'])
        if len(self.data["Subordinates"]) != 0:
            num = len(self.data["Subordinates"])
            for i in range(0, num):
                subordinate_Label = tk.Label(self.info_frame, text="Subordinate" + str(i+1))
                subordinate_Label.grid(row=(4*i)+10, column=0, padx=10, pady=10)
                
                sup_name_Label = tk.Label(self.info_frame, text="Name: ")
                sup_name_Label.grid(row=(4*i)+11, column=0, padx=10)
                sup_name_text = tk.Label(self.info_frame, text=self.data["Subordinates"][i]["FirstName"] + " " + self.data["Subordinates"][i]["LastName"])
                sup_name_text.grid(row=(4*i)+11, column=1, padx=10)
                
                sup_user_Label = tk.Label(self.info_frame, text="Username: ")
                sup_user_Label.grid(row=(4*i)+12, column=0, padx=10)
                sup_user_text = tk.Label(self.info_frame, text=self.data["Subordinates"][i]["Username"])
                sup_user_text.grid(row=(4*i)+12, column=1, padx=10)
                
                sup_posi_Label = tk.Label(self.info_frame, text="Position: ")
                sup_posi_Label.grid(row=(4*i)+13, column=0, padx=10)
                sup_posi_text = tk.Label(self.info_frame, text=self.data["Subordinates"][i]["Position"])
                sup_posi_text.grid(row=(4*i)+13, column=1, padx=10)
        
            delete_Button = tk.Button(self.info_frame, text="Delete", command=self.remove_employee)
            delete_Button.grid(row=(num*4)+14, column=0, pady=20)
            
            done_Button = tk.Button(self.info_frame, text="Done", command=self.done)
            done_Button.grid(row=(num*4)+14, column=1, pady=20)

        
        #if the new employee has no subordinates
        else:   
            delete_Button = tk.Button(self.info_frame, text="Delete", command=self.remove_employee)
            delete_Button.grid(row=10, column=0, pady=20)
            
            done_Button = tk.Button(self.info_frame, text="Done", command=self.done)
            done_Button.grid(row=10, column=1, pady=20)
            
            
    #When the 'Delete' button is pressed, this command is called
    #It will call the controller of the program and tell it to remove the selected employee from the database
    def remove_employee(self):
        self.controller.delete_employee(self.data["Employee"]["EmployeeID"])
        self.reset_frame()
        
        
    #This method will cause the program to return to the menu frame when the 'done' button is pressed
    #It will also clear the widgets in the info frame by calling the 'reset frame' method
    def done(self):
        self.controller.show_menu()
        self.reset_frame()
        
        
    #This method resets the frame by clearing all the widgets in the info frame
    #This will be called after the 'delete' or 'done' buttons are pressed
    def reset_frame(self):
        # Iterate through every widget inside the frame
        for widget in self.info_frame.winfo_children():
            widget.destroy()  # deleting widget
            
            




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
frame = deleteEmployeeFrame(root, data)
frame.grid()

# Run the main event loop
root.mainloop()
'''