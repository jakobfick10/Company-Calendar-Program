#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 22:35:26 2024

@author: jakobfick
"""


import tkinter as tk
from Manager_database_handler import ManagerDatabase
from ManagerLogginScreen import ManagerLoginFrame
from ManagerMenu import managerMenuFrame
from newEmployee import newEmployeeFrame
from searchSuperior import searchSuperiorFrame
from searchSubordinate import searchSubordinateFrame
from searchEmployee import searchEmployeeFrame
from ReviewEmployee import reviewEmployeeFrame
from deleteEmployee import deleteEmployeeFrame
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
        for F in (ManagerLoginFrame, managerMenuFrame, newEmployeeFrame, searchSuperiorFrame, searchSubordinateFrame, searchEmployeeFrame, deleteEmployeeFrame, reviewEmployeeFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)  # Passing 'self' as controller
            self.frames[page_name] = frame
            
        #self.main_frame = 'employeeDayFrame'
        
        
        # Show the login frame first
        self.show_login()
        '''
        
        #Login a John Doe automatically
        #change after development phase
        self.validate_credentials("john.doe@example.com", "password123")
        self.show_menu()
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
        
        
    def show_review(self):
        """Show the review employee frame."""
        self.show_frame("reviewEmployeeFrame")
        
    
    #This method is used to search for an employee in the database. When the user enters the username of an employee
    #into the search frame, this method will call a method in the database handler to find the selected employee, and
    #if the employees file is found, the delete Employee Frame will be displayed showing the selected employees info. If
    #no file is found, the program will display and error message
    def search_employee(self, email):
        #Searching for the selected employee
        employee, error = self.db.get_employee_hierarchy(email)
        
        #displaying the selected employee if they are found
        if employee:
            self.frames['deleteEmployeeFrame'].set_data(employee)
            self.frames['deleteEmployeeFrame'].widgets()
            self.show_delete()
        
        #displaying an error message if no employee is found
        else:
            if error == 1:
                self.frames["searchEmployeeFrame"].show_error("Issue Connecting to Database!")
            elif error == 2:
                self.frames["searchEmployeeFrame"].show_error("No Matching Employee Found!")
            else:
                self.frames["searchEmployeeFrame"].show_error("An Error Has Occured")
            
            
            
    #When the user enters the information of the new employee into the new employee frame and presses the enter button
    #This method will create a dictionary using the information entered and display the search superior frame
    def add_employee_1(self, first_name, last_name, username, password, role):
        self.new_employee = {"FirstName":first_name, "LastName":last_name, "Email":username, "Password":password, "Position":role, "Manager":None, "Subordinates":[]}
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
        self.show_review()
        self.frames["reviewEmployeeFrame"].show_employee(self.new_employee)
        
        
    def final_add_employee(self):
        print("employee has been added")
        self.db.add_employee_to_database(self.new_employee)
        self.show_menu()
        
    
    #This method when the user presses the 'Delete' button in the 'Delete Employee' frame
    #A method in the database handler will be called to remove the selected employee from the database
    def delete_employee(self, employeeID):
        #print(employeeID)
        self.db.remove_employee_from_database(employeeID)
        self.show_menu()
        

        
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
        

if __name__ == "__main__":
    db = ManagerDatabase(host="localhost", user="root", password="Mu!642724", database="EmployeeDB")


    # Create main application window
    root = tk.Tk()
    root.title("System")
    root.geometry("660x700")

    #creating the frame that will contain the login screen
    frame = MainApp(root, db)
    
    # Run the main event loop
    root.mainloop()