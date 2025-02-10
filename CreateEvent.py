#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 09:35:15 2024

@author: jakobfick
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta
from tkinter import messagebox

# This class is the create event frame. This frame will be displayed after user chooses to create a new event.
# The frame will display the a calendar, textboxes, and droppdown menues that will allow the user to enter
# information about the new event. When the user presses the 'create event' button, if no other events are
# scheduled during the chosen time, a new event will be added to the database. However, if the new event overlaps with
# an existing event, the GUI will display an error message.
class CreateEventFrame(tk.Frame):
    
    # Constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        #Placing this frame (CreateEventFrame) inside the widow
        #self.pack(fill="both", expand=1)
        
        #Setting the options for the dropdown menus that allow the user to select
        #the times of events.
        self.hour_Options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        self.min_Options = ["00", "10", "20", "30", "40", "50"]
        self.AMPM_Options = ["AM", "PM"]
        
        #Creating the variables that the date, start time, end time, and description will
        #be saved as.
        self.event_Date = datetime        #records the date (without the time) of the event
        self.start_Time = datetime        #records the start time (date and time) of the event
        self.end_Time = datetime          #records the end time (date and time) of the event
        self.start_Hour = tk.StringVar()
        self.start_Min = tk.StringVar()
        self.start_ampm = tk.StringVar()
        self.end_Hour = tk.StringVar()
        self.end_Min = tk.StringVar()
        self.end_ampm = tk.StringVar()
        
        # Calling the method that will create the different widgets in the frame
        self.widgets()
    
    #creating all the different widgets in the frame
    def widgets(self):
        # Creating the label that will instruct the user
        instructions = tk.Label(self, text="Enter the following information about the event. \n")
        instructions.grid(row=0, column=0, columnspan=6, padx=10, pady=10)
        
        # Creating the label that will instruct the user to select a date
        select_date = tk.Label(self, text="Select the date you wish to view!")
        select_date.grid(row=1, column=0, columnspan=7, padx=10, pady=10)
        
        # Create Calendar widget
        self.cal = Calendar(self, selectmode="day")
        self.cal.grid(row = 2, column=0, columnspan=7, pady=10)
        
        #Asking the user the start time of the event
        start_Label = tk.Label(self, text="Start Time: ")
        start_Label.grid(row=3, column=0, pady=10, sticky="w")
        start_Hour_Menu = tk.OptionMenu(self, self.start_Hour, *self.hour_Options)
        start_Hour_Menu.grid(row=3, column=1, sticky="w")
        colon1 = tk.Label(self, text=" : ")
        colon1.grid(row=3, column=2, sticky="w")
        start_Min_Menu = tk.OptionMenu(self, self.start_Min, *self.min_Options)
        start_Min_Menu.grid(row=3, column=3, sticky="w")
        comma1 = tk.Label(self, text=" , ")
        comma1.grid(row=3, column=4, sticky="w")
        start_M_Menu = tk.OptionMenu(self, self.start_ampm, *self.AMPM_Options)
        start_M_Menu.grid(row=3, column=5, sticky="w")
        
        #Asking the user the end time of the event
        end_Label = tk.Label(self, text="End Time: ")
        end_Label.grid(row=4, column=0, pady=10, sticky="w")
        end_Hour_Menu = tk.OptionMenu(self, self.end_Hour, *self.hour_Options)
        end_Hour_Menu.grid(row=4, column=1, sticky="w")
        colon2 = tk.Label(self, text=" : ")
        colon2.grid(row=4, column=2, sticky="w")
        end_Min_Menu = tk.OptionMenu(self, self.end_Min, *self.min_Options)
        end_Min_Menu.grid(row=4, column=3, sticky="w")
        comma2 = tk.Label(self, text=" , ")
        comma2.grid(row=4, column=4, sticky="w")
        end_M_Menu = tk.OptionMenu(self, self.end_ampm, *self.AMPM_Options)
        end_M_Menu.grid(row=4, column=5, sticky="w")
        
        #Providing a Textbox for the user to enter the event name
        name_Label = tk.Label(self, text="Event Name:")
        name_Label.grid(row=6, sticky="w")
        self.name_Box = tk.Text(self, width=40, height=2)
        self.name_Box.insert(1.0, "Event")
        self.name_Box.grid(row=7, columnspan=7)
        
        #Providing a Textbox for the user to enter the event description
        desc_Label = tk.Label(self, text="Description:")
        desc_Label.grid(row=8, sticky="w")
        self.desc_Box = tk.Text(self, width=40, height=5)
        self.desc_Box.grid(row=9, columnspan=7)
        
        #The button that will initiate the creation of the new event
        create_Button = tk.Button(self, text="Create Event", command=self.create_event)
        create_Button.grid(row=10, column=0, columnspan=3, padx=10, pady=10)
        
        #The button that will cancel the creation of the new event
        cancel_Button = tk.Button(self, text="Cancel", command=self.controller.show_frame("employeeDayFrame"))
        cancel_Button.grid(row=10, column=3, columnspan=3, padx=10, pady=10)
        
        #The Label that will display an error message if the scheduled time is invalid
        self.error_Label = tk.Label(self, text="")
        self.error_Label.grid(row=12, columnspan=6)
    
    
    #creating a new event using the data entered
    #currently it doesn't actually create an event object, it just prints the
    #start time and end time
    def create_event(self):
        complete = True
        if (not self.start_Hour.get()):
            complete = False
        elif(not self.start_Min.get()):
            complete = False
        elif(not self.start_ampm.get()):
            complete = False
        elif(not self.end_Hour.get()):
            complete = False
        elif(not self.end_Min.get()):
            complete = False
        elif(not self.end_ampm.get()):
            complete = False
            
        if complete:
               
            start_time = self.translateTime(self.start_Hour.get(), self.start_Min.get(), self.start_ampm.get())
            end_time = self.translateTime(self.end_Hour.get(), self.end_Min.get(), self.end_ampm.get())
            event_name = self.name_Box.get("1.0", "end-1c")
            #selected_date = self.cal.selection_get()
            selected_date = self.cal.get_date()
            event_date = datetime.strptime(selected_date, "%m/%d/%y").strftime('%Y-%m-%d')
            description = self.desc_Box.get("1.0", "end-1c")
            #messagebox.showinfo("Event Created", "Event Created\n" + str(self.start_Time) + "\n" + str(self.end_Time))
            self.controller.add_Event(event_name, event_date, start_time, end_time, description)

        else:
            messagebox.showerror("Error", "Error \nEnter a valid date and time!")
        
        
    #translating the time entered by the user into a timedate object
    def translateTime(self, hour, minute, ampm):
        if ampm == "AM":
            return "{}:{}".format(hour, minute)
        else:
            return "{}:{}".format(int(hour)+12, minute)
        

'''
# Create main application window
root = tk.Tk()
root.title("Create Event")
root.geometry("660x700")

#creating the frame that will contain the login screen
frame = CreateEventFrame(root)

# Run the main event loop
root.mainloop()
'''