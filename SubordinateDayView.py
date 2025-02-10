#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 10:29:18 2024

@author: jakobfick
"""

import tkinter as tk
from datetime import datetime, timedelta

# This class is the employee day frame. This frame will be displayed after am employee logs into
# the employee calendar program. The frame will display the schedule for the selected date (the current
# date will be selected by default). This frame will also provide buttons that will allow the user to
# perform certain actions, such as edit their schedule or log out.
class subordinateDayFrame(tk.Frame):
    
    # Constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        '''
        # Initialize schedule data, this is the list of events that will be displayed in the calendar
        # (example data. will use data from the database when completed)
        schedule = [
            {"start_time": "08:00", "end_time": "09:30", "event": "Meeting 1"},
            {"start_time": "10:00", "end_time": "11:30", "event": "Meeting 2"},
            {"start_time": "13:00", "end_time": "14:30", "event": "Lunch"},
            {"start_time": "15:00", "end_time": "16:30", "event": "Meeting 3"},
        ]
        '''

        #self.grid()
        
        #creating the previous day button
        prev_day = tk.Button(self, text="Prev Day", command=self.controller.show_prevDay)
        prev_day.grid(row = 0, column = 1, pady= 30)
        
        #creating the next day button
        next_day = tk.Button(self, text="Next Day", command=self.controller.show_nextDay)
        next_day.grid(row = 0, column = 3, pady= 30)
        
        #creating the add new event button
        new_event = tk.Button(self, wraplength=60, justify="center", text="Add New Event", command=self.controller.show_create_event)
        new_event.grid(row = 1, column = 0, padx=20)
        
        #creating the select date button
        select_date = tk.Button(self, wraplength=60, justify="center", text="Select Date", command=self.controller.show_select_date)
        select_date.grid(row = 2, column = 0, padx=20)
        
        #creating the view subordinate button
        view_sub = tk.Button(self, wraplength=80, justify="center", text="Return to my Calendar", command=self.controller.reset_dashboard)
        view_sub.grid(row = 3, column = 0, padx=10)
        
        #Creating the logout button
        logout = tk.Button(self, wraplength=60, justify="center", text="Logout", command=self.controller.logout)
        logout.grid(row = 4, column = 0, padx=20)
        
        #creating the canvas that will contain the day screen (everyting but scroll-bar)
        dayCanvas = tk.Canvas(self, width=500, height=600)
        dayCanvas.grid(row = 1, column = 1, rowspan = 4, columnspan=3, sticky="nsew") 
        
        # Create a Scrollbar widget
        scrollbar = tk.Scrollbar(self, orient="vertical", command=dayCanvas.yview)
        scrollbar.grid(row = 1, column = 4, rowspan=4, sticky="nsew") #pack(side="right", fill="y")
        
        # Attach the scrollbar to the datCanvas
        dayCanvas.config(yscrollcommand=scrollbar.set)
        dayCanvas.bind('<Configure>', lambda e: dayCanvas.configure(scrollregion=dayCanvas.bbox("all")))
        
        self.second_frame = tk.Frame(dayCanvas)
        dayCanvas.create_window((0, 0), window=self.second_frame, anchor="nw")

        # Create time grid with 5-minute increments
        self.time_labels = []
        start_time = datetime.strptime("00:00", "%H:%M")
        for i in range(24 * 6):  # 24 hours * 12 (5-minute increments per hour)
            if start_time.minute == 0:  # Only display whole hour times
                time_label = tk.Label(self.second_frame, text=start_time.strftime("%I:%M %p"))
                time_label.grid(row=i, column=1)
                self.time_labels.append(time_label)
                line = tk.Canvas(self.second_frame, width = 100, height = 2)
                line.config(bg="black")
                line.grid(row=i, column=2, sticky="n")
            else:
                time_label = tk.Label(self.second_frame, text=" ")
                time_label.grid(row=i, column=1)
            start_time += timedelta(minutes=10)

    def set_schedule(self, date, schedule):
        
        # Initialize schedule data (example data. will use data from the database when completed)
        self.schedule = schedule
        #print(schedule)
        
        #creating the label that displays the current date
        dateLabel = tk.Label(self, text=date)
        dateLabel.grid(row=0, column=2, pady= 30)

        # Display events
        for event_data in self.schedule:
            start_time = datetime.strptime(event_data["start_time"], "%H:%M")
            end_time = datetime.strptime(event_data["end_time"], "%H:%M")
            start_row = start_time.hour * 6  # Convert hour to row index
            start_row += start_time.minute // 10  # Adjust row index for 5-minute increments
            start_column = 50  # Adjust this value for horizontal position
            rowspan = (end_time - start_time).seconds // 600  # Calculate rowspan in 5-minute increments
            event_button = tk.Button(self.second_frame, text=event_data["event"], width=20, command=lambda e_id=event_data['event_id']: self.search_event_by_id(e_id))
            event_button.grid(column = 3, row=start_row, rowspan = rowspan, sticky="nsew")
            # Adjust relx and relwidth for horizontal size and position
            
    
    def search_event_by_id(self, event_id):
        print(event_id)
        self.controller.search_event_by_id(event_id)

        
    #Removes all event widgets from the DayScreen so the events can be reset
    def clear_DayScreen(self):
        # Loop through all children in the frame and destroy them if they are buttons
        for widget in self.second_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        
'''          
# Create main application window
root = tk.Tk()
root.title("Day View Calendar")
root.geometry("660x700")

#creating the frame that will contain the login screen
frame = employeeDayFrame(root, schedule)

# Run the main event loop
root.mainloop()
'''