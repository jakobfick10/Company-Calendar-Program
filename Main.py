#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 10:21:06 2024

@author: jakobfick
"""

import tkinter as tk
from LogginScreen import LoginFrame
from DayScreen import employeeDayFrame
from database_handler import EmployeeDatabase
from CreateEvent import CreateEventFrame
from ViewEvent import viewEventFrame
from SelectDate import selectDateFrame
from selectSubordinate import selectSubordinateFrame
from SubordinateDayView import subordinateDayFrame
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
        for F in (LoginFrame, employeeDayFrame, CreateEventFrame, viewEventFrame, selectDateFrame, selectSubordinateFrame, subordinateDayFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)  # Passing 'self' as controller
            self.frames[page_name] = frame
            
        self.main_frame = 'employeeDayFrame'
        
        
        # Show the login frame first
        self.show_login()
        '''
        
        #Login a John Doe automatically
        #change after development phase
        self.validate_credentials("jane.smith@example.com", "password456")
        self.show_dashboard()
        '''
        
    #Displays the Loging Page
    def show_login(self):
        """Show the login frame."""
        self.show_frame("LoginFrame")


    #Displays the DayScreen which shows the events of the selected day
    def show_dashboard(self):
        """Show the dashboard frame (employee day screen)."""
        self.frames[self.main_frame].set_schedule(datetime.now().strftime('%m-%d-%Y'), db.get_schedule_by_date(datetime.now().strftime('%Y-%m-%d')))
        self.show_frame(self.main_frame)
        
    
    #Displays the Create New Event Page
    def show_create_event(self):
        """Show the create new event frame."""
        self.show_frame("CreateEventFrame")
        
        
    #Displays the view Event Page
    def show_view_event(self):
        """Show the view event frame."""
        self.show_frame("viewEventFrame")
        
        
    #Displays the select date Page
    def show_select_date(self):
        """Show the view event frame."""
        self.show_frame("selectDateFrame")
        
        
    #Displays the select subordinate Page
    def show_select_subordinate(self):
        """Show the select subordinate frame."""
        self.show_frame("selectSubordinateFrame")
    
    
    #Changes the DayScreen from displaying the current day to the next day on the calendar
    #called when the next day button is pressed
    def show_nextDay(self):
        self.show_frame(self.main_frame)
        self.frames[self.main_frame].clear_DayScreen()
        date = db.get_next_day()
        self.frames[self.main_frame].set_schedule(date.strftime('%m-%d-%Y'), db.get_schedule_by_date(date.strftime('%Y-%m-%d')))
    
    
    #Changes the DayScreen from displaying the current day to the previous day on the calendar
    #called when the prev day button is pressed
    def show_prevDay(self):
        self.show_frame(self.main_frame)
        self.frames[self.main_frame].clear_DayScreen()
        date = db.get_prev_day()
        self.frames[self.main_frame].set_schedule(date.strftime('%m-%d-%Y'), db.get_schedule_by_date(date.strftime('%Y-%m-%d')))
        
        
    def show_date(self, date):
        self.show_frame(self.main_frame)
        self.frames[self.main_frame].clear_DayScreen()
        self.frames[self.main_frame].set_schedule(date.strftime('%m-%d-%Y'), db.get_schedule_by_date(date.strftime('%Y-%m-%d')))
            
            
    #Sends the command to the Database_handler to create a new event in the database
    def add_Event(self, event_name, event_date, start_time, end_time, description):
        '''
        event_name = "Math Class"
        date_str = '2024-09-29'
        event_date = datetime.strptime(date_str, '%Y-%m-%d')
        start_time = "12:00"
        end_time = "13:00"
        description = "Calculus 4 class in room 121"
        '''
        db.add_event(event_name, event_date, start_time, end_time, description)
        #reseting the DayScreen incase the event was added to the current day and then showing the DayScreen
        self.show_frame(self.main_frame)
        self.frames[self.main_frame].clear_DayScreen()
        current_date = datetime.strptime(self.db.date, "%Y-%m-%d").strftime("%m-%d-%Y")
        self.frames[self.main_frame].set_schedule(current_date, db.get_schedule_by_date(self.db.date))
        #self.frames[self.main_frame].set_schedule(self.db.date, db.get_schedule_by_date(self.db.date))
        #print(type(self.db.date))
        
        
    def search_event_by_id(self, event_id):
        """Search and display event details using the event_id from the database."""
        # Query the database for the event details using the event_id
        event = self.db.get_event_by_id(event_id)
        
        if event:
            # Display the event details along with the date and employee name
            event_info = (f"Event: {event['EventName']}\n"
                          f"Date: {event['EventDate']}\n"
                          f"Employee: {event['FirstName']} {event['LastName']}\n"
                          f"Start Time: {event['StartTime']}\n"
                          f"End Time: {event['EndTime']}\n"
                          f"Description: {event['Description']}\n")
            
            print(event_info)
            self.show_view_event()
            self.frames['viewEventFrame'].set_info(event_info, event_id)
        else:
            messagebox.showerror("Error", "Event not found.")
            #tk.Label(self.frame, text="Event not found.").pack()
            print("error")
            
            
    def delete_event_by_id(self, event_id):
        print(event_id)
        print("delete")
        self.db.delete_event(event_id)
        self.show_frame(self.main_frame)
        self.frames[self.main_frame].clear_DayScreen()
        self.frames[self.main_frame].set_schedule(self.db.date, db.get_schedule_by_date(self.db.date))
        
        
    def get_subordinates(self):
        print(self.db.get_subordinates())
        subordinates = self.db.get_subordinates()
        self.frames["selectSubordinateFrame"].widgets(subordinates)
        self.show_select_subordinate()
        
        
    def display_subordinates(self, ID):
        self.db.set_subordinate_ID(ID)
        self.main_frame = 'subordinateDayFrame'
        """Show the dashboard frame (subordinate day screen)."""
        self.show_dashboard()
        '''
        self.frames['subordinateDayFrame'].set_schedule(datetime.now().strftime('%m-%d-%Y'), db.get_schedule_by_date(datetime.now().strftime('%Y-%m-%d')))
        self.show_frame("subordinateDayFrame")
        '''
        
    
    def reset_dashboard(self):
        self.db.reset_employee_ID()
        self.main_frame = 'employeeDayFrame'
        self.show_dashboard()
        
        
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
        result, error = self.db.validate_password(username, password)
        if result:
            self.show_dashboard()
        elif error == 1:
            self.frames['LoginFrame'].show_error("Username does not Exist")
        elif error == 2:
            self.frames['LoginFrame'].show_error("Incorrect Password")
        else:
            self.frames['LoginFrame'].show_error("An Error has Occured")
            
            
    def logout(self):
        self.db.logout()
        self.frames['LoginFrame'].clear_text()
        self.frames[self.main_frame].clear_DayScreen()
        self.show_login()
        

if __name__ == "__main__":
    db = EmployeeDatabase(host="localhost", user="root", password="Mu!642724", database="EmployeeDB")


    # Create main application window
    root = tk.Tk()
    root.title("Calendar")
    root.geometry("660x700")

    #creating the frame that will contain the login screen
    frame = MainApp(root, db)
    
    # Run the main event loop
    root.mainloop()
    

