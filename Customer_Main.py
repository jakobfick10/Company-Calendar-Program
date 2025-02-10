#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 13:55:56 2024

@author: jakobfick
"""

import tkinter as tk
from Customer_database_handler import CustomerDatabase
from CustomerMenu import customerMenuFrame
from Customer_Date import customerDateFrame
from Customer_Time import customerTimeFrame
from datetime import datetime
from tkinter import messagebox

class MainApp(tk.Tk):
    def __init__(self, root, db):
        #tk.Tk.__init__(self)
        #self.title("Employee Management System")
        #self.geometry("660x700")

        self.db = db
        self.root = root

        # Using grid for the container
        container = root

        self.frames = {}
        '''
        # Configure grid layout for expanding the frames
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        '''
        # Initialize frames but don't show them immediately
        for F in (customerMenuFrame, customerDateFrame, customerTimeFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)  # Passing 'self' as controller
            self.frames[page_name] = frame
            
        self.main_frame = 'customerMenuFrame'
        

        # Show the login frame first
        self.show_menu()
     
    #Displays the menu Page
    def show_menu(self):
        """Show the login frame."""
        self.show_frame("customerMenuFrame")
        
    #Displays the select date Page
    def show_date(self):
        """Show the login frame."""
        self.show_frame("customerDateFrame")
        
    #Displays the select time Page
    def show_time(self):
        """Show the login frame."""
        self.show_frame("customerTimeFrame")
    
    '''
    #Displays the Loging Page
    def show_login(self):
        """Show the login frame."""
        self.show_frame("ManagerLoginFrame")
        
        
    #Displays the Loging Page
    def show_menu(self):
        """Show the menu frame."""
        self.show_frame("managerMenuFrame")
        
    #Displays the new employee frame
    def show_new_employee(self):
        """Show the new employee frame."""
        self.show_frame("newEmployeeFrame")
        
        
    #Displays the search SuperiorFrame frame
    def show_search_superior(self):
        """Show the search superior frame."""
        self.show_frame("searchSuperiorFrame")
        
        
    #Displays the search SuperiorFrame frame
    def show_search_subordinate(self):
        """Show the search subordinate frame."""
        self.show_frame("searchSubordinateFrame")
    
        
    #Displays the search employee frame
    def show_search(self):
        """Show the search employee frame."""
        self.show_frame("searchEmployeeFrame")
        
        
    #Displays the delete employee frame
    def show_delete(self):
        """Show the delete employee frame."""
        self.show_frame("deleteEmployeeFrame")
        
    '''
    def find_meeting_times(self, date):
        company_reps = self.db.find_meeting_times(date)
        time_available = False
        
        #Checking if there is at least 1 available time slot
        for rep in company_reps:
            if rep.get("Slots"):
                time_available = True
        
        if time_available:
            print("available")
            print(company_reps)
            self.show_time()
            self.frames["customerTimeFrame"].display_times(company_reps, date)
            
        else:
            print("None Available")
            
    #Adding a meeting to the selected company representative's schedule
    def add_meeting(self, rep_ID, time, date):
        print(rep_ID)
        print(date)
        print(time)
        event_name = "Customer Meeting"
        event_desc = "Meeting with a customer."
        start_time, end_time = time.split(" - ")
        start_time = self.convert_to_24_hour(start_time)
        end_time = self.convert_to_24_hour(end_time)
        print(start_time)
        print(end_time)
        result = self.db.add_event(rep_ID, event_name, date, start_time, end_time, event_desc)
        self.show_menu()
        if result:
            self.frames['customerMenuFrame'].display_success()
        else:
            self.frames['customerMenuFrame'].display_failure()

        
        
    # Define a function to convert 12-hour time to 24-hour time
    def convert_to_24_hour(self, time_str):
        # Parse the time string into a datetime object
        time_obj = datetime.strptime(time_str, "%I:%M %p")
        # Format the datetime object into a 24-hour time string
        return time_obj.strftime("%H:%M")

        
            
    '''
    
    def search_employee(self, email):
        employee = self.db.get_employee_hierarchy(email)
        if employee:
            self.frames['deleteEmployeeFrame'].set_data(employee)
            self.frames['deleteEmployeeFrame'].widgets()
            self.show_delete()
            
    #When the user enters the information of the new employee into the new employee frame and presses the enter button
    #This method will create a dictionary using the information entered and display the search superior frame
    def add_employee_1(self, first_name, last_name, username, password, role):
        self.new_employee = {"FirstName":first_name, "LastName":last_name, "Username":username, "Password":password, "Position":role, "Manager":None, "Subordinates":[]}
        print(self.new_employee)
        self.show_search_superior()
        
    #When a new employee is being added to the database, this method will be sent the username of their superior,
    #search the database for the superiors file, and if found add them to the new employees file
    def add_employee_2(self, username):
        superior  = self.db.get_employee_info(username)
        if superior == None:
            self.frames["searchSuperiorFrame"].show_error("No Employee Found!")
        else:
            self.new_employee["Manager"] = superior
            print(self.new_employee)
            self.show_search_subordinate()
            
            
    #When a new employee is being added to the database, this method will be sent the username of one of thier subordinates,
    #search the database for the subordinates file, and if found add them to the new employees file
    def add_employee_subordinate(self, username):
        subordinate  = self.db.get_employee_info(username)
        if subordinate == None:
            self.frames["searchSubordinateFrame"].show_error("No Employee Found!")
        else:
            self.new_employee["Subordinates"].append(subordinate)
            print(self.new_employee)
            self.frames["searchSubordinateFrame"].show_success("Subordinate added to \nnew employee's file.")
            
            
    #This method finalizes the new employee data and then displays the frame that will show the user the final
    #verson of the new employee file
    def review_new_employee(self):
        print(self.new_employee)
    '''
        
    #Shows the selected frame by moving it to 'the top of the list and hiding the others
    def show_frame(self, page_name):
        """Raise and display the selected frame."""
        # Hide all frames first by gridding them out of sight
        for frame in self.frames.values():
            frame.grid_remove()

        # Show the selected frame
        frame = self.frames[page_name]
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()  # Bring the selected frame to the front

    '''       
    def validate_credentials(self, username, password):        
        """Handles validation and queries the database for employee details."""
        result = self.db.validate_password(username, password)
        if result:
            self.show_menu()
        else:
            self.frames['ManagerLoginFrame'].show_error("Login Failed")
            
            
    def logout(self):
        self.db.logout()
        self.frames['ManagerLoginFrame'].clear_text()
        self.show_login()
    '''   

if __name__ == "__main__":
    db = CustomerDatabase(host="localhost", user="root", password="Mu!642724", database="EmployeeDB")


    # Create main application window
    root = tk.Tk()
    root.title("System")
    root.geometry("660x700")

    #creating the frame that will contain the login screen
    frame = MainApp(root, db)
    
    # Run the main event loop
    root.mainloop()